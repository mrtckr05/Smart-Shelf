import asyncio

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models import Inventory, Product

from app.services.confirmation_service import get_consensus
from app.services.observation_service import (
    create_observation_from_counts
)


MONITOR_INTERVAL = 10
CONFIRMATION_INTERVAL = 1.5
CONFIRMATION_SAMPLES = 5


class MonitoringService:

    def __init__(
        self,
        camera_manager,
        shelf_id: int
    ):
        self.camera_manager = camera_manager
        self.shelf_id = shelf_id

        self.running = False
        self.task = None

    def start(self):

        if self.running:
            return

        self.running = True

        self.task = asyncio.create_task(
            self.run()
        )

    async def run(self):

        while self.running:

            try:
                await self.monitor_once()

            except Exception as e:

                print(
                    f"Monitoring error: {e}"
                )

            await asyncio.sleep(
                MONITOR_INTERVAL
            )

    async def monitor_once(self):

        counts = (
            self.camera_manager
            .get_latest_counts()
        )

        if not counts:
            return

        db = SessionLocal()

        try:

            inventory = self._get_inventory(
                db
            )

            if not self._has_changed(
                inventory,
                counts
            ):
                return

        finally:

            db.close()

        print(
            "Inventory değişikliği tespit edildi."
        )

        await self.confirm_change()

    def _get_inventory(self, db):

        statement = select(
            Inventory,
            Product.class_name
        ).join(
            Product,
            Inventory.product_id == Product.id
        ).where(
            Inventory.shelf_id == self.shelf_id
        )

        rows = db.execute(
            statement
        ).all()

        return {
            class_name: inventory.quantity
            for inventory, class_name in rows
        }

    def _has_changed(
        self,
        inventory,
        counts
    ):

        for class_name, quantity in counts.items():

            current_quantity = inventory.get(
                class_name
            )

            if current_quantity != quantity:
                return True

        return False

    async def confirm_change(self):

        confirmation_counts = []

        for i in range(
            CONFIRMATION_SAMPLES
        ):

            counts = (
                self.camera_manager
                .get_latest_counts()
            )

            if counts:

                confirmation_counts.append(
                    counts.copy()
                )

                self._save_observation(
                    counts
                )

            if i < CONFIRMATION_SAMPLES - 1:

                await asyncio.sleep(
                    CONFIRMATION_INTERVAL
                )

        if not confirmation_counts:
            return

        consensus = get_consensus(
            confirmation_counts
        )

        print(
            f"Confirmation sonucu: {consensus}"
        )

        await self.apply_consensus(
            consensus
        )

    def _save_observation(
        self,
        counts
    ):

        db = SessionLocal()

        try:

            create_observation_from_counts(
                db=db,
                shelf_id=self.shelf_id,
                counts=counts
            )

        finally:

            db.close()

    async def apply_consensus(
        self,
        consensus
    ):

        db = SessionLocal()

        try:

            for class_name, quantity in consensus.items():

                statement = select(
                    Inventory
                ).join(
                    Product,
                    Inventory.product_id == Product.id
                ).where(
                    Inventory.shelf_id == self.shelf_id,
                    Product.class_name == class_name
                )

                inventory = db.scalar(
                    statement
                )

                if inventory is None:

                    product_statement = select(
                        Product
                    ).where(
                        Product.class_name == class_name
                    )

                    product = db.scalar(
                        product_statement
                    )

                    if product is None:
                        continue

                    inventory = Inventory(
                        shelf_id=self.shelf_id,
                        product_id=product.id,
                        quantity=quantity
                    )

                    db.add(inventory)

                else:

                    inventory.quantity = quantity

            db.commit()

            print(
                f"Inventory güncellendi: {consensus}"
            )

        finally:

            db.close()

    async def stop(self):

        self.running = False

        if self.task is not None:

            await self.task

            self.task = None
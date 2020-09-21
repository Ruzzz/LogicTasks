import logging

from catsauction.models.meta import db
from catsauction.models.models import Animals, Bet, Lot, User

logger = logging.getLogger(__name__)


class AuctionService:

    async def add_lot(self, price, animal_id, current_user_id):
        animal = await Animals.get(animal_id)
        if animal is None or animal.owner_id != current_user_id:
            raise ValueError()

        lot = await Lot.create(price=price, animal_id=animal_id, owner_id=current_user_id)
        return lot.id

    async def add_bet(self, value, lot_id, current_user_id):
        lot = await Lot.get(lot_id)
        if lot is None or lot.owner_id == current_user_id:
            raise ValueError()

        bet = await Bet.create(value=value, lot_id=lot_id, owner_id=current_user_id)
        return bet.id

    async def takes_bet(self, bet_id, current_user_id):
        async with db.transaction() as tx:
            bet = await Bet.get(bet_id)
            if bet is None or bet.owner_id == current_user_id:
                raise ValueError()

            lot = await Lot.get(bet.lot_id)

            seller = await User.get(current_user_id)
            await seller.update(balance=seller.balance + lot.price).apply()

            # TODO: Check buyer balance
            buyer = await User.get(bet.owner_id)
            await buyer.update(balance=buyer.balance - lot.price).apply()

            animal = await Animals.get(lot.animal_id)
            await animal.update(owner_id=buyer.id).apply()

            await Bet.delete.where(Bet.lot_id == lot.id).gino.status()
            await lot.delete()


auction_service = AuctionService()

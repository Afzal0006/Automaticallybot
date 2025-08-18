from pyrogram import Client, filters
import config, db, blockchain

app = Client("escrowbot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# ✅ Help command
@app.on_message(filters.command("help"))
async def help_command(_, msg):
    text = """
🤖 *Escrow Bot Commands*

/newdeal @buyer <amount>  
➡️ Create a new deal between seller and buyer.  

/fund <deal_id> <tx_hash>  
➡️ Buyer confirms payment by giving transaction hash.  

/release <deal_id> <seller_wallet>  
➡️ Release funds from escrow to seller (after buyer approval).  

/help  
➡️ Show this help menu.  
"""
    await msg.reply(text, quote=True)

# ✅ New deal
@app.on_message(filters.command("newdeal"))
async def newdeal(_, msg):
    try:
        _, buyer, amount = msg.text.split()
        deal_id = str(msg.id)

        deal = {
            "deal_id": deal_id,
            "buyer": buyer,
            "seller": msg.from_user.username,
            "amount": float(amount),
            "status": "pending"
        }
        db.create_deal(deal)
        await msg.reply(f"✅ Deal Created!\nDeal ID: {deal_id}\nBuyer: {buyer}\nAmount: {amount} USDT\n\nBuyer must send to: `{config.ESCROW_ADDRESS}`")
    except:
        await msg.reply("Usage: /newdeal @buyer 100")

# ✅ Fund confirmation
@app.on_message(filters.command("fund"))
async def fund(_, msg):
    try:
        _, deal_id, tx_hash = msg.text.split()
        deal = db.get_deal(deal_id)

        if blockchain.verify_payment(tx_hash, deal["amount"]):
            db.update_deal(deal_id, {"status": "funded", "tx_hash": tx_hash})
            await msg.reply(f"✅ Payment verified! Funds are in escrow.")
        else:
            await msg.reply("❌ Payment not found / invalid transaction.")
    except:
        await msg.reply("Usage: /fund deal_id txhash")

# ✅ Release funds
@app.on_message(filters.command("release"))
async def release(_, msg):
    try:
        _, deal_id, seller_address = msg.text.split()
        deal = db.get_deal(deal_id)

        if deal["status"] != "funded":
            await msg.reply("❌ Deal not funded yet.")
            return

        tx_hash = blockchain.release_funds(seller_address, deal["amount"])
        db.update_deal(deal_id, {"status": "released", "release_tx": tx_hash})
        await msg.reply(f"✅ Funds released to {seller_address}\nTx: {tx_hash}")
    except Exception as e:
        await msg.reply(f"Error: {str(e)}")

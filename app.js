const { Telegraf } = require("telegraf");
const path = require("path");

require("dotenv").config({ path: path.join(__dirname, ".env") });

const { CommandHandler } = require("./src/handlers/commandHandler");
const { CallbackHandler } = require("./src/handlers/callbackHanldler");

const bot = new Telegraf(process.env.BOT_TOKEN);

CommandHandler(bot);
CallbackHandler(bot);

bot.launch();

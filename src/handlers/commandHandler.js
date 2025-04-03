const { message } = require("telegraf/filters");
const { InlineKeyboard } = require("../buttons");
module.exports.CommandHandler = (bot) => {
  bot.start(async (ctx) => {
    await ctx.replyWithHTML("TG bot for RSS", InlineKeyboard.buttons_start());
  });
  bot.help((ctx) => ctx.reply("Send me a sticker"));

  bot.on(message("sticker"), (ctx) => ctx.reply("👍"));
  bot.hears("hi", (ctx) => ctx.reply("Hey there"));
};

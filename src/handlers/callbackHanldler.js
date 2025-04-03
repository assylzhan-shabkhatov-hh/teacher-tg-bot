const { message } = require("telegraf/filters");
const Parser = require("rss-parser");
const { InlineKeyboard } = require("../buttons");
const parser = new Parser();

module.exports.CallbackHandler = (bot) => {
  bot.on("callback_query", async (ctx) => {
    const { callbackQuery } = ctx;
    console.log(callbackQuery);

    if (callbackQuery.data == "redit RSS") {
      const feed = await parser.parseURL("https://www.reddit.com/.rss");

      const newsMessageText = feed.items.map((item) => item.title).join("\n\n");

      await ctx.editMessageText(`news from reddit: \n\n ${newsMessageText}`);
    }
    if (callbackQuery.data == "list RSS") {
      await ctx.editMessageText(
        "Select source :",
        InlineKeyboard.buttons_source()
      );
    }
  });
};

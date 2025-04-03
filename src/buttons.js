const { Markup } = require("telegraf");

module.exports.InlineKeyboard = {
  buttons_start: () => {
    return Markup.inlineKeyboard([
      [Markup.button.callback("Список RSS", "list RSS")],
    ]);
  },
  buttons_source: () => {
    return Markup.inlineKeyboard([
      [Markup.button.callback("Reddit", "redit RSS")],
    ]);
  },
  buttons_back: () => {
    return Markup.inlineKeyboard([[Markup.button.callback("Back", "back")]]);
  },
};

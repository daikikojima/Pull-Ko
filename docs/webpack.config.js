const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = [
{
  /* ----------------
     JS用モジュール
    ----------------- */
  entry: {
    main: "./src/js/index.js"
  },
  output: {
    path: path.resolve(__dirname, "dist/js"),
    publicPath: '/js/',
    filename: "[name].js"
  },
  plugins: [
    /* use jQuery as Global */
    new webpack.ProvidePlugin({
        jQuery: "jquery",
        $: "jquery",
        'window.jQuery': 'jquery',
        Popper: ['popper.js', 'default'],
    })
  ],
  resolve: {
    extensions: ['.js']
  }
},
{
  /* ----------------
     CSS用モジュール
    ----------------- */
  entry: {
    main: "./src/style/app.scss"
  },
  output: {
    path: path.resolve(__dirname, "dist/css"),
    publicPath: '/css/',
    filename: "[name].css"
  },
  module: {
    rules: [
      // Sassファイルの読み込みとコンパイル
      {
        test: /\.scss$/,
        exclude: /node_modules/,
        // ローダー名

        use: [
          MiniCssExtractPlugin.loader,
          // CSSをバンドルするための機能
          {
            loader: 'css-loader',
            options: {
            },
          },
          // PostCSS
          {
            loader: "postcss-loader",
            options: {
              plugins: function () {
                return [
                  require('precss'),
                  require('autoprefixer')
                ];
              }
            }
          },

          // Sassをバンドルするための機能
          {
            loader: 'sass-loader',
            options: {
            }
          }
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: './[name].css'
    })
  ],
  resolve: {
    // style-loader の中で、.jsファイルを拡張子なしで requireしているところがあるため、'.js'が必要
    extensions: ['.css', '.js']
  },
}
];
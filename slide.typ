#import "@preview/touying:0.7.4": *
#import themes.simple: *

#show: simple-theme.with(aspect-ratio: "16-9")

= PythonでLinuxデスクトッププログラミング

= Linuxデスクトップ

// Linuxの個人環境というとコンソールでコマンドラインシェルを使うをイメージすることが多い。
// UNIX哲学でUNIXコマンドをパイプでつないで活用する話も有名。
// WSLはGUIも提供するようになったが基本的にはコマンドラインシェルを提供するものだった。
// GnomeやKDEといったLinuxデスクトップはGUIだけでなくユーザーセッションや各種サービスを提供している。
// Linuxデスクトップで画像や動画といったマルチメディアも取り扱える。

== Linuxでデスクトップ環境を使おう

- Linuxのイメージ
  - suckless
  - Unix as IDE
  - UNIX哲学
  - WSL
  - sshの先でtmuxが動いてるやつ
- デスクトップ環境は必要でしょう
  - 画像や動画も取り扱う時代
  - 外部デバイス

== Linuxデスクトップ

- だいたいgnomeというもののことだと思ってください
  - それ以外を使う人はわかってる人でしょ
- デスクトップを支えるものたち
  - gvfs
  - secret manager
  - notification
  - タスクバー
  - アプリケーションランチャー

== Linuxデスクトッププログラミングとgobject

- glib/gobject
  - C言語のライブラリ
  - オブジェクト指向を実現するもの
  - クラス、インターフェイス
  - プロパティ
  - シグナル
  - プロパティバインディング
- gnome関連のコンポーネントはgobjectで作られている
  - gnome-shell
  - evolution-data-server

== GObjectなマルチメディアライブラリ

- gdk-pixbuf
  - 画像処理のライブラリ
  - 退役予定らしい
  - gdk textureなどを使うようにとのことである
  - pythonでやるときはPillow使うだけなので気にしない
- gstreamer
  - 動画や音声の再生録画など
  - ミキシングやリサンプリングなどのパイプライン
- poppler
  - PDFのライブラリ
  - 旧xpdf
  - glibラッパーがありgiを提供している

= pythonで書こう

// GObjectはC言語でオブジェクト指向を実現しているがマクロやキャストが多く快適とは言い難い。
// giによって各種言語へのバインディグが提供される。
// PyGObjectはGObjectのオブジェクト指向をPythonの文法に適合させている。
// PyGObjectを使うと快適にLinuxデスクトップアプリケーションを実装できる。

== GObject辛い

- C言語でオブジェクト指向
- マクロやキャストの嵐
- メソッドは名前空間からフルで全部書く
- リファレンスカウントを増減させる関数は自分で呼ぶ
- 文字列結合程度でもfreeとか気にしないといけない
- エラー処理はGErrorのポインタをポインタで渡す

== 辛い

```c
   GtkWidget *win = gtk_application_window_new(app);
   gtk_window_set_child(GTK_WINDOW(win), child);
   gtk_window_present(win);
```

== C以外で書きたい！GObject Introspection

- gobjectで実装したライブラリを様々な言語から使う
- 命名規約に従っていればうまいことやってくれる
- 従ってないならがんばってコメントに設定を書く
- 主要なライブラリはgiを提供している

== PyGObject

- GObjectのオブジェクト指向機能をPython文法で書ける
- giが提供されてるならこの仕組みでそのままimport可能
- クラス定義はそのまま
- プロパティやシグナルはデコレーターなどで実装
- エラー処理も例外処理に変換される

== pygtkではないのか？

- pygtkはgtk2まで
- ライブラリごとにバインディングを作っていた
- 今はPyGObject経由でgtk4などを呼ぶようになっている

```py
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Poppler", "0.18")

import cairo
from gi.repository import Gio, GLib, GObject, Gtk, Poppler
```

== 実例：Counter Model (1/2)

- count intプロパティ

```python
class CounterModel(GObject.Object):
    @GObject.Property(type=int, flags=GObject.ParamFlags.READABLE)
    def count(self):
        return self._count

    def do_constructed(self):
        self._count = 0
```

== 実例：Counter Model (2/2)

- incrementメソッド
- decrementメソッド

```python
    def increment(self):
        self._count += 1
        self.notify("count")

    def decrement(self):
        self._count += 1
        self.notify("count")
```

- リードオンリーのプロパティを内部で更新したらnotifyメソッドでsignalを出す

== 実例：Counter View

- CounterModelのプロパティやメソッドを紐づける
    - counter_label.label - model.count
    - increment_button.clicked - model.increment
    - decrement_button.clicked - model.decrement

```py
        self.model.bind_property("count", self.count_label, "label", GObject.BindingFlags.SYNC_CREATE)
        self.increment_button.connect("clicked", lambda *args: self.model.increment())
        self.decrement_button.connect("clicked", lambda *args: self.model.decrement())
```
= Popplerを使ってPDFリーダーをつくる

// 実際にPyGObjectを使う例としてPDFリーダーを作る。
// Popplerもgiを提供している。
// Popplerはページの内容をcairo surfaceとしてレンダリングする。
// GtkではDrawingAreaを使ってcairo surfaceを画面表示できる。

== cairo surface

- cairoはgiを提供していないがPyGObjectではpycairoを特別扱いしてくれる
- いい感じの表示になるようサイズ計算
  - aspect ratio
- cairo contextでscale指定
- Image Surface をcairo contextのsourceに指定
- cairo contextにpaintで反映
```py
        d = min(width / w, height / h)
        cr.scale(d, d)
        cr.set_source_surface(self.surface, 0, 0)
        cr.paint()
```

== poppler

- ~Poppler.Document~ でPDFファイルをロードする
- documentからページごとに ~Poppler.Page~ オブジェクトを取得する
- レンダリング先のImage Surfaceを作る
  - キャッシュするため
- pageのrenderメソッドでページ内容をレンダリング

```py
            self.surface = cairo.ImageSurface(cairo.Format.ARGB32, int(w), int(h))
            c = cairo.Context(self.surface)
            self.page.render(c)
```
== Gtk.DrawingArea

- drwaing functionでcairo contextを使った描画方法を指定できる
- Gtk.Widgetのサブクラスなのでqueue_drawで再描画を要求できる
- ページ変更シグナルに対応してqueue_drawする


== 参考文献

- https://docs.gtk.org/, GTK Documentation
- https://gi.readthedocs.io/en/latest/, GObject Introspection
- https://pygobject.gnome.org/, PyGObject
- https://poppler.freedesktop.org/, Poppler
- https://poppler.freedesktop.org/api/glib/, Poppler glib
- https://www.cairographics.org/, Cairo

# Grace

## 项目简介

> Grace - Make your programming graceful

Grace 是一款开发助手软件，旨在让的开发工作更加轻松和优雅。

## 开始

从 Python 官网下载 Python 3.11 安装包并安装。

项目虚拟环境是通过 pipenv 来管理的，通过 `pip` 命令安装 pipenv。

```commandline
pip install pipenv
```

设置环境变量 `PIPENV_VENV_IN_PROJECT` 的值为 `1`，保证虚拟环境的路径在项目的根目录下。

通过 git 拉取项目。

```commandline
git clone git@github.com:zhuuuoyue/Grace.git
```

进入项目，并安装依赖。

```commandline
cd grace
pipenv install
```

安装完成后，双击项目根目录下 `start.bat` 批处理文件即可打开程序。

## 继续开发

### 项目结构

项目的主要模块有：

- `command` - 命令模块，负责定义命令的接口、注册和管理命令。
- `db` - 数据库模块，负责数据的维护和查询。
- `tasks` - 业务模块，负责各荐具体的业务，不包含界面。
- `ui` - 用户界面模块，负责定义命令和界面、用户交互。
- `exts` - 拓展模块，除 `main.py` 外，其他模块不得依赖于此模块。
- `context.py` - 上下文模块。
- `main.py` - 主入口。

`tasks`、`ui`、`exts` 的联系与区别：

- 三者都提供了软件的功能。
- `tasks` - 开发最通用的一些功能，如版本控制、文件创建等，只包含功能，不包含界面，不得依赖于 `ui` 和 `exts` 模块。
- `ui` - 软件界面、交互，定义命令，依赖于 `tasks` 模块，但不得依赖 `exts` 模块。
- `exts` - 拓展模块，定义一个特别的功能，有别于通用的功能，如某家公司对开发的特殊要求。

### 添加功能

在项目根目录下的 `ui.json` 中配置软件界面，其中定义了 menu 和 action。

```json
{
    "modules": [
        {
            "title": "VCS",
            "tooltip": "",
            "commands": [
                {
                    "command_id": "cmd_edit_repositories",
                    "title": "Edit Repositories",
                    "icon": "",
                    "tooltip": ""
                }
            ]
        }
    ]
}
```

在 `ui` 模块下添加命令，并在 `ui/__init__.py` 中将其注册。

### 添加拓展

可以以 module 和 package 的形式拓展程序功能。

通过 `initialize` 初始化函数来注册拓展模块，`initialize` 函数原型为：

```python
from shared.context import Context


def initialize(ctx: Context):
    pass
```

初始化函数的位置：

- 若是 module，如 `hello.py`，则直接在 py 文件中定义初始化函数。
- 若是 package，如 `hello/`，则在 `__init__.py` 文件中定义初始化函数。

如何初始化？

- 为了让新添加的拓展功能在命令模式的工作流中得以运行，须将命令实例化并注册。
- 为了让用户访问到，须添加界面的 menu 和 action。

```python
from command import register_command
from shared.context import Context
from ui import Action, MainWindow

from .hello import HelloCommand


def initialize(ctx: Context):
    register_command('cmd_hello', HelloCommand())

    win = ctx.main_window
    if isinstance(win, MainWindow):
        mb = win.menuBar()
        m = mb.addMenu('demo')
        win.add_action('demo', Action('cmd_hello', 'Hello', m))
```

Gomoku
======

测试五子棋(无禁手)AI.

已有 ai_arrowrowe(0), ai_sway(1) 两份 AI.

ai_user(2) 为用户输入, ai_random(3) 为随机.

### 运行

```bash
python gomoku_platform.py         # ai0 和 ai1 轮流执黑各进行一局.
python gomoku_platform.py x       # aix 和自己进行一局.
python gomoku_platform.py x, y    # aix 执黑与 aiy 进行一局.
```

### 如何写一份新AI:

1. 新建.py文件, 内容示例及函数意义附后. 假设名为 `ai_new.py`.

2. 在 `gomoku_platform.py` 开头添加 `import ai_new as ai4`(数字递增)

3. 修改 `ai_new.py`.

```python
class Gomoku:
    def __init__(self, n, index, name='ai_new'):
        "生成nxn棋盘, 我方执黑(0)或白(1), 名为name."
        self.n = n
        self.index = index
        self.name = name

    def receive(self, x, y):
        "对方落子(x, y), 如何回应? 返回(i, j)表示在该点落子, 返回 None 表示认输."
        pass

    def start(self):
        "我方开局, 返回(i, j)表示在该点落子."
        pass
```

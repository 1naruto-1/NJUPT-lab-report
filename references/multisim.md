# Multisim 仿真与真实截图（用 multisim-cli）

工具本身的用法、网表和布局写法见 multisim-cli skill（`~/.claude/skills/multisim-cli/SKILL.md` 和其 `references/spec.md`）。这里只写本课程的做法。命令统一是：

```
python -m multisim_cli <命令> ...
```

## 流程

1. 在该次实验文件夹下建 `multisim/`，每个电路写一个 spec.json（输出 .ms14 也放这里，文件名用英文）。
2. `python -m multisim_cli build xx.json --preview xx_preview.png`：看预览图和 `warnings`，`problems` 必须为空。导线穿过元件、交叉多就改坐标重来。
3. `python -m multisim_cli sim xx.ms14 ...` 取仿真数值，填“理论值 / 仿真值”对比表。
4. 提醒用户约一分钟内不要动鼠标键盘，再 `python -m multisim_cli capture xx.ms14 multisim/shots`。逐张看图，不合适就调 instruments / sim_time 重新 build 再截。
5. 报告里放 `<stem>_circuit.png`（电路）和仪器面板图（`_XSC1.png`、`_XBP1.png` 等），需要时放整屏截图 `_screen.png`。

## 本课程常用电路的写法

- 信号源：交流用 `V1 vin 0 DC 0 AC 1 SIN(0 <峰值> <频率>)`（要做频率特性必须带 `AC 1`）；方波用 `PULSE(...)`。实验要求用函数发生器时才用 XFG。
- 示波器：`XSC1 <A通道> <B通道> 0 nc1 0 nc2 OSCILLOSCOPE`，A 通道接输入、B 通道接输出；B 通道导线默认蓝色、波形也是蓝色。时基让一屏显示 2～3 个周期，`trigger` 用 `none`，`sim_time` 取一屏时长的整数倍并长于 5τ。
- 波特图仪：`XBP1 vin 0 vout 0 BODE`。幅频、相频各生成一个文件（mode 分别为 magnitude、phase）各截一次；横轴 `log`，纵轴线性 0～1 最直观（`vertical: lin, lin_min: 0, lin_max: 1`），带通/谐振电路按峰值调 `lin_max`。频率单位可以写 `1MHz`、`100kHz`。
- 频率特性的数值：`sim xx.ms14 --ac 10,1MEG,100 --out vout --in vin --at <理论截止频率>`，`cutoff` 给出 -3 dB 频率和该处相位，`peak` 给出谐振频率和峰值增益；上下限频率、带宽、Q 都从这里算。
- 晶体管/运放电路：`sim --op --nets b,c,e` 得到静态工作点；`--tran` 得到输出峰峰值、周期，`--ac` 得到中频增益和截止频率。LM324AJ、LM555CN 等用的是真实模型，饱和、削顶都能算出来。
- 两端元件 0° 横放、第一个节点在左；90° 竖放、第一个节点在上（并联到地的元件写 90）。多引脚器件先 `parts show <型号>` 看引脚位置。
- 课本型号在库里没有时 `parts fetch <型号>`（如 `LM555CN`、`74LS00N`、`UA741CD`）；数据库里也没有的国产型号（9013、9012 等）用相近型号代替（如 2N2222A、2N2907A），并在报告里注明“仿真中以 ×× 代替”。

## 已知限制

- 波特图仪、示波器的读数光标不能预设，截图上光标停在起点；转折频率等数值写在图题或正文里（来自 `sim`），并提醒用户课上自己拖游标读数。
- 截不到图（Multisim 打不开、面板不弹出等）时：说明情况，请用户在 Multisim 里手动打开生成的 .ms14、按 F5 运行后截图，不要用别的方式造图。

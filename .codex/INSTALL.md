# 在 Codex 中安装 GamePowers

一次性安装 `GamePowers + superpowers + beads(bd)`。

- GitHub 仓库：`https://github.com/yangwuan55/gamepowers`
- 在线安装文档：`https://raw.githubusercontent.com/yangwuan55/gamepowers/refs/heads/main/.codex/INSTALL.md`

## 前置条件

- Git
- Python 3
- `pip`
- macOS/Linux 的 `bash` 环境

## 安装步骤

1. **克隆 GamePowers 仓库：**
   ```bash
   git clone https://github.com/yangwuan55/gamepowers.git ~/.codex/gamepowers
   cd ~/.codex/gamepowers
   ```

2. **运行一键安装脚本：**
   ```bash
   ./tools/install_all.sh
   ```

   该脚本会自动安装或更新：
   - `beads`（`bd` 命令）
   - `superpowers`（路径：`~/.codex/superpowers`）
   - skills 软链（`~/.agents/skills/superpowers -> ~/.codex/superpowers/skills`）
   - 当前 `gamepowers` 包（`pip install -e .`）
   - `bd init`（当仓库还没有 `.beads` 时）

3. **重启 Codex**，让 skills 发现机制生效。

## 验证安装

```bash
bd version
gamepowers --help
ls -la ~/.agents/skills/superpowers
```

可选验证：

```bash
cd ~/.codex/gamepowers
python3 tools/validate_skills_contract.py --repo-root ~/.codex/gamepowers
```

## 更新

```bash
cd ~/.codex/gamepowers
git pull --ff-only
./tools/install_all.sh
```

## 卸载

```bash
rm -f ~/.agents/skills/superpowers
rm -rf ~/.codex/superpowers
python3 -m pip uninstall -y gamepowers
```

可选：删除本地 GamePowers 仓库

```bash
rm -rf ~/.codex/gamepowers
```

## 说明

- `./tools/install_all.sh --dry-run`：仅预览执行动作。
- `./tools/install_all.sh --skip-bd-init`：跳过仓库 `bd init`。

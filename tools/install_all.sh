#!/usr/bin/env bash
set -euo pipefail

# One-shot installer for GamePowers + superpowers + beads(bd).
# - Installs/updates bd (beads CLI)
# - Installs/updates superpowers and links skills for Codex discovery
# - Installs current GamePowers package in editable mode
# - Initializes bd in this repo if not initialized

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CODEX_HOME="${CODEX_HOME:-${HOME}/.codex}"
AGENTS_HOME="${AGENTS_HOME:-${HOME}/.agents}"
SUPERPOWERS_DIR="${CODEX_HOME}/superpowers"
SUPERPOWERS_SKILLS_LINK="${AGENTS_HOME}/skills/superpowers"
SUPERPOWERS_SKILLS_TARGET="${SUPERPOWERS_DIR}/skills"
GAMEPOWERS_SKILLS_LINK="${AGENTS_HOME}/skills/gamepowers"
GAMEPOWERS_SKILLS_TARGET="${REPO_ROOT}/skills"

DRY_RUN=0
SKIP_BD_INIT=0

usage() {
  cat <<'USAGE'
Usage: tools/install_all.sh [options]

Options:
  --dry-run       Print actions without executing them
  --skip-bd-init  Do not run "bd init" in this repository
  -h, --help      Show this help
USAGE
}

log() {
  echo "[install_all] $*"
}

run_cmd() {
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] $*"
    return 0
  fi
  "$@"
}

run_shell() {
  local command="$1"
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[dry-run] ${command}"
    return 0
  fi
  bash -lc "${command}"
}

ensure_symlink() {
  local link_path="$1"
  local target_path="$2"
  local display_name="$3"

  run_cmd mkdir -p "$(dirname "${link_path}")"

  if [[ -L "${link_path}" ]]; then
    local current_target
    current_target="$(readlink "${link_path}" || true)"
    if [[ "${current_target}" != "${target_path}" ]]; then
      log "更新 ${display_name} 软链: ${link_path} -> ${target_path}"
      run_cmd rm -f "${link_path}"
      run_cmd ln -s "${target_path}" "${link_path}"
    fi
    return
  fi

  if [[ -e "${link_path}" ]]; then
    echo "${display_name} 目标已存在且不是软链: ${link_path}" >&2
    exit 1
  fi

  log "创建 ${display_name} 软链: ${link_path} -> ${target_path}"
  run_cmd ln -s "${target_path}" "${link_path}"
}

install_bd() {
  if command -v bd >/dev/null 2>&1; then
    log "bd 已安装: $(bd version | head -n1)"
    return
  fi

  if command -v brew >/dev/null 2>&1; then
    log "检测到 Homebrew，尝试安装 beads (bd)"
    if ! run_cmd brew install beads; then
      log "brew install beads 失败，回退到官方脚本安装"
      run_shell 'curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash'
    fi
  else
    log "未检测到 Homebrew，使用官方脚本安装 beads (bd)"
    run_shell 'curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash'
  fi

  if [[ "${DRY_RUN}" -eq 0 ]]; then
    command -v bd >/dev/null 2>&1 || {
      echo "bd 安装后不可用，请检查 PATH" >&2
      exit 1
    }
    log "bd 安装完成: $(bd version | head -n1)"
  fi
}

install_or_update_superpowers() {
  log "安装/更新 superpowers 到 ${SUPERPOWERS_DIR}"
  run_cmd mkdir -p "${CODEX_HOME}"

  if [[ -d "${SUPERPOWERS_DIR}/.git" ]]; then
    run_cmd git -C "${SUPERPOWERS_DIR}" pull --ff-only
  elif [[ -e "${SUPERPOWERS_DIR}" ]]; then
    echo "路径已存在但不是 git 仓库: ${SUPERPOWERS_DIR}" >&2
    exit 1
  else
    run_cmd git clone https://github.com/obra/superpowers.git "${SUPERPOWERS_DIR}"
  fi

  ensure_symlink "${SUPERPOWERS_SKILLS_LINK}" "${SUPERPOWERS_SKILLS_TARGET}" "superpowers skills"
}

install_gamepowers() {
  if [[ ! -d "${GAMEPOWERS_SKILLS_TARGET}" ]]; then
    echo "GamePowers skills 目录不存在: ${GAMEPOWERS_SKILLS_TARGET}" >&2
    exit 1
  fi

  ensure_symlink "${GAMEPOWERS_SKILLS_LINK}" "${GAMEPOWERS_SKILLS_TARGET}" "gamepowers skills"

  log "安装当前 GamePowers（editable）"
  if run_cmd python3 -m pip install -e "${REPO_ROOT}"; then
    return
  fi

  log "标准 pip 安装失败，尝试 --break-system-packages"
  if run_cmd python3 -m pip install --break-system-packages -e "${REPO_ROOT}"; then
    return
  fi

  log "警告：GamePowers CLI 安装失败，但 skills 软链已完成，可在 Codex 中发现并使用。"
  log "如需 CLI，请使用虚拟环境：python3 -m venv .venv && source .venv/bin/activate && pip install -e ."
}

init_bd_repo() {
  if [[ "${SKIP_BD_INIT}" -eq 1 ]]; then
    log "跳过 bd init"
    return
  fi

  if [[ -d "${REPO_ROOT}/.beads" ]]; then
    log "检测到 ${REPO_ROOT}/.beads，跳过 bd init"
    return
  fi

  log "在仓库初始化 bd: ${REPO_ROOT}"
  run_cmd bd init "${REPO_ROOT}"
}

main() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      --skip-bd-init)
        SKIP_BD_INIT=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "未知参数: $1" >&2
        usage
        exit 1
        ;;
    esac
  done

  install_bd
  install_or_update_superpowers
  install_gamepowers
  init_bd_repo

  log "安装完成。请重启 Codex 以确保 superpowers skills 被发现。"
  log "可用命令检查：bd version && gamepowers --help"
}

main "$@"

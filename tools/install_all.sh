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

  log "配置 superpowers skills 软链到 ${SUPERPOWERS_SKILLS_LINK}"
  run_cmd mkdir -p "${AGENTS_HOME}/skills"

  if [[ -L "${SUPERPOWERS_SKILLS_LINK}" ]]; then
    local current_target
    current_target="$(readlink "${SUPERPOWERS_SKILLS_LINK}" || true)"
    if [[ "${current_target}" != "${SUPERPOWERS_SKILLS_TARGET}" ]]; then
      run_cmd rm -f "${SUPERPOWERS_SKILLS_LINK}"
      run_cmd ln -s "${SUPERPOWERS_SKILLS_TARGET}" "${SUPERPOWERS_SKILLS_LINK}"
    fi
  elif [[ -e "${SUPERPOWERS_SKILLS_LINK}" ]]; then
    echo "目标已存在且不是软链: ${SUPERPOWERS_SKILLS_LINK}" >&2
    exit 1
  else
    run_cmd ln -s "${SUPERPOWERS_SKILLS_TARGET}" "${SUPERPOWERS_SKILLS_LINK}"
  fi
}

install_gamepowers() {
  log "安装当前 GamePowers（editable）"
  run_cmd python3 -m pip install -e "${REPO_ROOT}"
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

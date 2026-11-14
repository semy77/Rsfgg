# ═══════════════════════════════════════════════════════════════════════════
#  main.py — SEMY EDITION (AUTO-REPEAT ∞)
#  1 Match → End → all connections closed → 3s off → repeat ∞ (cache reuses login)
#  Owner: SEMY | Telegram: @SEMY
# ═══════════════════════════════════════════════════════════════════════════

import sys
import asyncio
import time


_OWNER_NAME = "SEMY"
_TG_ID = "@SEMY"

COOLDOWN_AFTER_MATCH = 3.0   # cleanup grace before next round


def _show_banner():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   █████╗ ███╗   ██╗██╗   ██╗██████╗  █████╗  ██████╗         ║
║  ██╔══██╗████╗  ██║██║   ██║██╔══██╗██╔══██╗██╔════╝         ║
║  ███████║██╔██╗ ██║██║   ██║██████╔╝███████║██║  ███╗        ║
║  ██╔══██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║██║   ██║        ║
║  ██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║  ██║╚██████╔╝        ║
║  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝         ║
║                                                              ║
║  SINGH EDITION — All Regions Support (AUTO-REPEAT ∞)         ║
║                                                              ║
║  Owner      : {_OWNER_NAME:<46}║
║  Telegram   : {_TG_ID:<46}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def _close_leaked_aiohttp():
    """Safety net: close aiohttp session if match.py somehow leaked it."""
    try:
        from match import _aiohttp_session as _m_sess
        if _m_sess is not None and not _m_sess.closed:
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(_m_sess.close())
            finally:
                loop.close()
    except Exception:
        pass


def run_match_loop():
    """Infinite loop: round N → close all → 3s cooldown → round N+1."""
    from match import start_match_interactive

    match_round = 0
    while True:
        match_round += 1
        print()
        print("  ╔══════════════════════════════════════════╗")
        print(f"  ║       MATCH ROUND #{match_round:<3}                 ║")
        print("  ╚══════════════════════════════════════════╝")
        print()

        try:
            asyncio.run(start_match_interactive())

            print()
            print("  ✅ Round complete — all connections closed.")
            print(f"  ⏳ Cooling down {COOLDOWN_AFTER_MATCH:.0f}s before next round...")
            time.sleep(COOLDOWN_AFTER_MATCH)

        except KeyboardInterrupt:
            print()
            print("  🛑 Ctrl+C — stopping auto-repeat loop.")
            raise   # propagate up to menu

        except Exception as e:
            print()
            print(f"  X Round #{match_round} error: {e}")
            import traceback
            traceback.print_exc()
            print(f"  ⏳ Retrying in {COOLDOWN_AFTER_MATCH:.0f}s...")
            time.sleep(COOLDOWN_AFTER_MATCH)
        finally:
            _close_leaked_aiohttp()


def main_menu():
    _show_banner()
    while True:
        print()
        print("  ╔══════════════════════════════════════════╗")
        print("  ║         MAIN MENU  BY SEMY               ║")
        print("  ╠══════════════════════════════════════════╣")
        print("  ║  1. Start Match (auto-repeat ∞)          ║")
        print("  ║  2. Exit                                 ║")
        print("  ╚══════════════════════════════════════════╝")
        print()

        try:
            choice = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("  👋 Bye.")
            break

        if choice == "1":
            try:
                run_match_loop()
            except KeyboardInterrupt:
                print()
                print("  ↩  Auto-repeat stopped — returning to menu...")
                time.sleep(1.0)
                continue
        elif choice == "2":
            print()
            print("  👋 Bye.")
            break
        else:
            print("  ! Invalid choice")

        print()
        try:
            input("  Press Enter to return to menu...")
        except (EOFError, KeyboardInterrupt):
            print()
            print("  👋 Bye.")
            break


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n  👋 interrupted — exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
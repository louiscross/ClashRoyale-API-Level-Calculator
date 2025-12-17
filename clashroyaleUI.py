import threading
import tkinter as tk
from tkinter import ttk, messagebox

import requests

from API import Main


class ClashRoyaleCalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Clash Royale Level Calculator")
        self.root.geometry("1100x780")
        self.root.minsize(980, 720)

        self._setup_style()

        self.session = requests.Session()
        self.state = {
            "player_tag": "",
            "token": "",
            "player_name": "",
            "trophies": 0,
            "king_level": 0,
        }
        self.last_results = None
        self.last_upgrade_events = None

        self._build_shell()
        self.show_connect()

    def _setup_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background="#0f172a")
        style.configure("Card.TFrame", background="#111827")
        style.configure("Title.TLabel", background="#0f172a", foreground="#e5e7eb", font=("Segoe UI", 18, "bold"))
        style.configure("H2.TLabel", background="#111827", foreground="#e5e7eb", font=("Segoe UI", 12, "bold"))
        style.configure("Body.TLabel", background="#111827", foreground="#cbd5e1", font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background="#111827", foreground="#94a3b8", font=("Segoe UI", 9))
        style.configure("Link.TLabel", background="#0f172a", foreground="#60a5fa", font=("Segoe UI", 9, "underline"))

        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Secondary.TButton", font=("Segoe UI", 10))

        style.configure("TEntry", padding=6)
        style.configure("TSpinbox", padding=6)
        style.configure("TProgressbar", thickness=12)
        style.configure(
            "Current.Horizontal.TProgressbar",
            troughcolor="#0b1220",
            background="#22c55e",
            bordercolor="#0b1220",
            lightcolor="#22c55e",
            darkcolor="#22c55e",
        )
        style.configure(
            "Result.Horizontal.TProgressbar",
            troughcolor="#0b1220",
            background="#60a5fa",
            bordercolor="#0b1220",
            lightcolor="#60a5fa",
            darkcolor="#60a5fa",
        )

    def _build_shell(self) -> None:
        self.container = ttk.Frame(self.root, style="App.TFrame")
        self.container.pack(fill="both", expand=True)

        self.header = ttk.Frame(self.container, style="App.TFrame")
        self.header.pack(fill="x", padx=18, pady=(16, 8))

        self.title_label = ttk.Label(self.header, text="Clash Royale Level Calculator", style="Title.TLabel")
        self.title_label.pack(side="left")

        self.header_right = ttk.Frame(self.header, style="App.TFrame")
        self.header_right.pack(side="right")

        self.status_var = tk.StringVar(value="Not connected")
        self.status_label = ttk.Label(self.header_right, textvariable=self.status_var, style="Link.TLabel")
        self.status_label.pack(side="right")

        self.content = ttk.Frame(self.container, style="App.TFrame")
        self.content.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _clear_content(self) -> None:
        for w in self.content.winfo_children():
            w.destroy()

    def show_connect(self) -> None:
        self._clear_content()
        self.status_var.set("Not connected")

        card = ttk.Frame(self.content, style="Card.TFrame", padding=18)
        card.pack(fill="x", pady=(0, 12))

        ttk.Label(card, text="Connect", style="H2.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Enter your Player Tag and API Token. The token is only used locally to call the official API.",
            style="Body.TLabel",
            wraplength=900,
        ).pack(anchor="w", pady=(6, 14))

        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(fill="x")

        self.player_tag_var = tk.StringVar(value="")
        self.token_var = tk.StringVar(value="")

        ttk.Label(form, text="Player Tag", style="Body.TLabel").grid(row=0, column=0, sticky="w")
        tag_entry = ttk.Entry(form, textvariable=self.player_tag_var)
        tag_entry.grid(row=1, column=0, sticky="we", padx=(0, 12), pady=(4, 10))
        ttk.Label(form, text="Example: UU8R2V8J (with or without #)", style="Muted.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 12)
        )

        ttk.Label(form, text="API Token", style="Body.TLabel").grid(row=0, column=1, sticky="w")
        token_entry = ttk.Entry(form, textvariable=self.token_var, show="•")
        token_entry.grid(row=1, column=1, sticky="we", pady=(4, 10))
        ttk.Label(form, text="From developer.clashroyale.com", style="Muted.TLabel").grid(row=2, column=1, sticky="w")

        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=(16, 0))

        self.connect_btn = ttk.Button(actions, text="Validate & Continue", style="Primary.TButton", command=self._connect)
        self.connect_btn.pack(side="left")

        ttk.Button(actions, text="Quit", style="Secondary.TButton", command=self.root.destroy).pack(side="left", padx=10)

        tag_entry.focus_set()

        help_card = ttk.Frame(self.content, style="Card.TFrame", padding=18)
        help_card.pack(fill="x")
        ttk.Label(help_card, text="What this tool calculates", style="H2.TLabel").pack(anchor="w")
        ttk.Label(
            help_card,
            text=(
                "It simulates upgrading cards from your collection to estimate how far your King Level can progress "
                "given your available Gold and card copies (and optional Wild Cards)."
            ),
            style="Body.TLabel",
            wraplength=900,
        ).pack(anchor="w", pady=(6, 0))

    def _normalize_player_tag(self, raw: str) -> str:
        tag = (raw or "").strip().upper()
        if tag.startswith("#"):
            tag = tag[1:]
        return tag

    def _connect(self) -> None:
        player_tag = self._normalize_player_tag(self.player_tag_var.get())
        token = "".join((self.token_var.get() or "").split())

        if (not player_tag) or (not player_tag.isalnum()) or (len(player_tag) not in (7, 8, 9)):
            messagebox.showerror("Invalid Player Tag", "Player tag must be 7, 8, or 9 characters (letters/numbers).")
            return
        if not token:
            messagebox.showerror("Invalid Token", "Please enter a Clash Royale API token.")
            return

        self.connect_btn.configure(state="disabled")
        self.status_var.set("Validating credentials...")

        t = threading.Thread(target=self._connect_worker, args=(player_tag, token), daemon=True)
        t.start()

    def _connect_worker(self, player_tag: str, token: str) -> None:
        try:
            url = f"https://api.clashroyale.com/v1/players/%23{player_tag}"
            headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
            response = self.session.get(url, headers=headers, timeout=15)
            if not response.ok:
                if response.status_code == 404:
                    raise RuntimeError("Player not found. Check the tag and try again.")
                if response.status_code in (401, 403):
                    raise RuntimeError("Token invalid or not authorized for your IP.")
                raise RuntimeError(f"API error {response.status_code}: {response.reason}")

            data = response.json()
            self.state.update(
                {
                    "player_tag": player_tag,
                    "token": token,
                    "player_name": data.get("name", ""),
                    "trophies": data.get("trophies", 0),
                    "king_level": data.get("expLevel", 0),
                }
            )
            self.root.after(0, self.show_calculator)
        except Exception as e:
            # In Python 3, exception variables are cleared at the end of the except block.
            # Pass the message as an argument to avoid late-binding issues in callbacks.
            self.root.after(0, self._connect_failed, str(e))

    def _connect_failed(self, msg: str) -> None:
        self.connect_btn.configure(state="normal")
        self.status_var.set("Not connected")
        messagebox.showerror("Connection Failed", msg)

    def show_calculator(self) -> None:
        self._clear_content()
        self.status_var.set(f"Connected: {self.state['player_name']}  (#{self.state['player_tag']})")

        top = ttk.Frame(self.content, style="App.TFrame")
        top.pack(fill="x", pady=(0, 12))

        identity = ttk.Frame(top, style="Card.TFrame", padding=16)
        identity.pack(side="left", fill="x", expand=True, padx=(0, 12))

        ttk.Label(identity, text="Player", style="H2.TLabel").pack(anchor="w")
        self.player_line_var = tk.StringVar(
            value=f"{self.state['player_name']}  •  Trophies: {self.state['trophies']:,}  •  King Level: {self.state['king_level']}"
        )
        ttk.Label(identity, textvariable=self.player_line_var, style="Body.TLabel").pack(anchor="w", pady=(6, 6))

        bars = ttk.Frame(identity, style="Card.TFrame")
        bars.pack(fill="x")
        bars.grid_columnconfigure(0, weight=1)

        ttk.Label(bars, text="Current progress to next level", style="Muted.TLabel").grid(row=0, column=0, sticky="w")
        self.current_progress_var = tk.DoubleVar(value=0.0)
        self.current_progress = ttk.Progressbar(
            bars, variable=self.current_progress_var, maximum=100, style="Current.Horizontal.TProgressbar"
        )
        self.current_progress.grid(row=1, column=0, sticky="we", pady=(6, 2))
        self.current_progress_text_var = tk.StringVar(value="")
        ttk.Label(bars, textvariable=self.current_progress_text_var, style="Muted.TLabel").grid(
            row=2, column=0, sticky="w"
        )

        actions = ttk.Frame(top, style="Card.TFrame", padding=16)
        actions.pack(side="right")

        ttk.Button(actions, text="Change Account", style="Secondary.TButton", command=self.show_connect).pack(
            fill="x", pady=(0, 8)
        )
        ttk.Button(actions, text="Refresh", style="Secondary.TButton", command=self._recalculate).pack(fill="x")

        body = ttk.Frame(self.content, style="App.TFrame")
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body, style="Card.TFrame", padding=16)
        left.pack(side="left", fill="y", padx=(0, 12))

        right = ttk.Frame(body, style="Card.TFrame", padding=16)
        right.pack(side="right", fill="both", expand=True)

        self._build_inputs(left)
        self._build_outputs(right)

        self._recalculate()

    def _build_inputs(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Inputs", style="H2.TLabel").pack(anchor="w")
        ttk.Label(parent, text="Gold Budget", style="Body.TLabel").pack(anchor="w", pady=(12, 0))

        self.gold_var = tk.StringVar(value="0")
        gold_entry = ttk.Entry(parent, textvariable=self.gold_var)
        gold_entry.pack(fill="x", pady=(4, 0))
        ttk.Label(parent, text="Tip: enter 999999999 to simulate 'unlimited' gold.", style="Muted.TLabel").pack(
            anchor="w", pady=(4, 0)
        )

        sep = ttk.Separator(parent)
        sep.pack(fill="x", pady=14)

        ttk.Label(parent, text="Wild Cards (optional)", style="Body.TLabel").pack(anchor="w")
        ttk.Label(
            parent,
            text="Only Wild Cards are supported in calculations (Books/Elite/Coins were removed/converted).",
            style="Muted.TLabel",
            wraplength=260,
        ).pack(anchor="w", pady=(4, 8))

        self.wc_vars = {
            "common": tk.StringVar(value="0"),
            "rare": tk.StringVar(value="0"),
            "epic": tk.StringVar(value="0"),
            "legendary": tk.StringVar(value="0"),
            "champion": tk.StringVar(value="0"),
        }

        grid = ttk.Frame(parent, style="Card.TFrame")
        grid.pack(fill="x")

        labels = [
            ("Common", "common"),
            ("Rare", "rare"),
            ("Epic", "epic"),
            ("Legendary", "legendary"),
            ("Champion", "champion"),
        ]

        for r, (label, key) in enumerate(labels):
            ttk.Label(grid, text=label, style="Body.TLabel").grid(row=r, column=0, sticky="w", pady=4)
            ttk.Entry(grid, textvariable=self.wc_vars[key], width=12).grid(row=r, column=1, sticky="e", pady=4)

        grid.grid_columnconfigure(0, weight=1)

        self.run_btn = ttk.Button(parent, text="Recalculate", style="Primary.TButton", command=self._recalculate)
        self.run_btn.pack(fill="x", pady=(16, 0))

    def _build_outputs(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Results", style="H2.TLabel").pack(anchor="w")

        self.summary_frame = ttk.Frame(parent, style="Card.TFrame")
        self.summary_frame.pack(fill="x", pady=(12, 12))

        self.result_title_var = tk.StringVar(value="Waiting for calculation...")
        ttk.Label(self.summary_frame, textvariable=self.result_title_var, style="Body.TLabel").pack(anchor="w")

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress = ttk.Progressbar(
            self.summary_frame, variable=self.progress_var, maximum=100, style="Result.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x", pady=(10, 4))

        self.progress_text_var = tk.StringVar(value="")
        ttk.Label(self.summary_frame, textvariable=self.progress_text_var, style="Muted.TLabel").pack(anchor="w")

        stats = ttk.Frame(parent, style="Card.TFrame")
        stats.pack(fill="x")

        self.stats_vars = {
            "max_level": tk.StringVar(value="-"),
            "gold_spent": tk.StringVar(value="-"),
            "gold_remaining": tk.StringVar(value="-"),
            "xp_gained": tk.StringVar(value="-"),
            "upgrades": tk.StringVar(value="-"),
        }

        def add_stat(col: int, title: str, var_key: str) -> None:
            box = ttk.Frame(stats, style="Card.TFrame", padding=10)
            box.grid(row=0, column=col, sticky="nsew", padx=6)
            ttk.Label(box, text=title, style="Muted.TLabel").pack(anchor="w")
            ttk.Label(box, textvariable=self.stats_vars[var_key], style="H2.TLabel").pack(anchor="w", pady=(4, 0))

        add_stat(0, "Max King Level", "max_level")
        add_stat(1, "Gold Spent", "gold_spent")
        add_stat(2, "Gold Remaining", "gold_remaining")
        add_stat(3, "XP Gained", "xp_gained")
        add_stat(4, "Upgrades", "upgrades")

        for i in range(5):
            stats.grid_columnconfigure(i, weight=1)

        details = ttk.Frame(parent, style="Card.TFrame", padding=10)
        details.pack(fill="both", expand=True, pady=(12, 0))

        header = ttk.Frame(details, style="Card.TFrame")
        header.pack(fill="x")

        self.details_mode_var = tk.StringVar(value="milestones")

        title = ttk.Label(header, text="Per-level gold milestones (cumulative)", style="Muted.TLabel")
        title.pack(side="left")

        toggle = ttk.Frame(header, style="Card.TFrame")
        toggle.pack(side="right")

        ttk.Button(toggle, text="Milestones", command=lambda: self._set_details_mode("milestones")).pack(
            side="left", padx=(0, 6)
        )
        ttk.Button(toggle, text="Upgrade Path", command=lambda: self._set_details_mode("upgrades")).pack(side="left")

        self.details_list = tk.Listbox(details, height=12)
        self.details_list.configure(
            bg="#0b1220",
            fg="#e5e7eb",
            selectbackground="#1f2937",
            selectforeground="#e5e7eb",
            highlightthickness=0,
            relief="flat",
            activestyle="none",
        )
        self.details_list.pack(fill="both", expand=True, pady=(6, 0))

    def _set_details_mode(self, mode: str) -> None:
        self.details_mode_var.set(mode)
        self._render_details()

    def _render_details(self) -> None:
        self.details_list.delete(0, tk.END)
        if not self.last_results:
            self.details_list.insert(tk.END, "No calculation yet.")
            return

        mode = self.details_mode_var.get()
        if mode == "upgrades":
            events = self.last_upgrade_events or []
            if not events:
                self.details_list.insert(tk.END, "No upgrades performed in this simulation.")
                return
            for ev in events:
                gold_part = f"  (gold {ev['goldCost']:,})" if ev.get("goldCost") is not None else ""
                self.details_list.insert(
                    tk.END, f"{ev['cardName']}: Level {ev['fromLevel']} → {ev['toLevel']}{gold_part}"
                )
            return

        milestones = self.last_results.get("perLevelCumulativeGold") or []
        if not milestones:
            self.details_list.insert(tk.END, "No king level-ups achieved in this simulation.")
            return
        for item in milestones:
            self.details_list.insert(
                tk.END, f"Reached King Level {item['level']}: {item['cumulativeGold']:,} gold spent"
            )

    @staticmethod
    def _parse_int(text: str) -> int:
        s = (text or "").strip()
        if not s:
            return 0
        digits = "".join(ch for ch in s if ch.isdigit())
        return int(digits) if digits else 0

    def _collect_inputs(self) -> tuple[int, dict]:
        gold = self._parse_int(self.gold_var.get())
        wildcards = {k: self._parse_int(v.get()) for k, v in self.wc_vars.items()}
        return gold, wildcards

    def _recalculate(self) -> None:
        self.run_btn.configure(state="disabled")
        self.result_title_var.set("Calculating...")
        self.progress_var.set(0.0)
        self.progress_text_var.set("")
        self.last_results = None
        self.last_upgrade_events = None
        self.details_list.delete(0, tk.END)

        gold, wildcards = self._collect_inputs()

        worker = threading.Thread(target=self._calc_worker, args=(gold, wildcards), daemon=True)
        worker.start()

    def _calc_worker(self, available_gold: int, wildcards: dict) -> None:
        try:
            player_tag = self.state["player_tag"]
            token = self.state["token"]

            main_instance = Main(player_tag, token)
            response = self.session.get(
                f"https://api.clashroyale.com/v1/players/%23{player_tag}",
                headers=main_instance.headers,
                timeout=15,
            )
            if response.status_code != 200:
                raise RuntimeError(f"Failed to fetch player data: {response.status_code}")

            player_data = response.json()

            account = main_instance.getAccount(player_data)
            account.gold = max(0, int(available_gold))

            exp_table = main_instance.exp_table([])
            upgrade_table = main_instance.upgrade_table([])
            upgrade_table_exp = main_instance.upgrade_table_exp([])
            card_required_table = main_instance.card_required_table([])

            cards = player_data.get("cards", [])
            card_data = main_instance.getCards(cards, [])
            card_data = sorted(card_data, key=lambda c: c.level)

            total_gold_spent = 0
            total_xp_gained = 0
            upgrades_performed = 0
            per_level_cumulative_gold = []
            upgrade_events = []

            def safe_to_int(value) -> int:
                s = str(value)
                if s.upper() == "N/A":
                    return 0
                digits = "".join(ch for ch in s if ch.isdigit())
                return int(digits) if digits else 0

            def rarity_index_from_max_level(max_level: int) -> int:
                # Post-update mapping (Level 16):
                # Common=16, Rare=14, Epic=11, Legendary=8, Champion=6
                if max_level == 16:
                    return 1
                if max_level == 14:
                    return 2
                if max_level == 11:
                    return 3
                if max_level == 8:
                    return 4
                if max_level == 6:
                    return 5
                # Legacy fallback
                if max_level == 14:
                    return 1
                if max_level == 12:
                    return 2
                if max_level == 9:
                    return 3
                if max_level == 6:
                    return 4
                if max_level == 4:
                    return 5
                return 1

            def rarity_key_from_max_level(max_level: int) -> str:
                if max_level in (16, 14):  # common or rare depending on era; index mapping handles details
                    # In the post-update mapping, 16 is common and 14 is rare. For legacy, 14 is common.
                    return "common" if max_level == 16 else "rare"
                if max_level == 11:
                    return "epic"
                if max_level == 8:
                    return "legendary"
                if max_level == 6:
                    return "champion"
                if max_level == 12:
                    return "rare"
                if max_level == 9:
                    return "epic"
                if max_level == 4:
                    return "champion"
                return "common"

            def try_cover_with_wildcards(required: int, current: int, rarity_key: str) -> tuple[bool, int]:
                deficit = max(0, required - current)
                if deficit <= 0:
                    return True, current
                available = wildcards.get(rarity_key, 0)
                use = min(deficit, available)
                wildcards[rarity_key] = available - use
                current += use
                return current >= required, current

            max_card_level = 16

            while card_data:
                c = card_data[0]

                if c.level >= max_card_level:
                    card_data.pop(0)
                    continue

                rarity_index = rarity_index_from_max_level(c.maxLevel)
                next_level_index = c.level
                if next_level_index >= len(card_required_table):
                    card_data.pop(0)
                    continue

                required_cards = safe_to_int(card_required_table[next_level_index][rarity_index])
                rarity_key = rarity_key_from_max_level(c.maxLevel)

                can_upgrade, adjusted_count = try_cover_with_wildcards(required_cards, int(c.count), rarity_key)
                c.count = adjusted_count
                if not can_upgrade:
                    card_data.pop(0)
                    continue

                c.count = int(c.count) - required_cards
                from_level = int(c.level)
                c.level = from_level + 1
                upgrades_performed += 1

                row_idx = c.level - 1
                gold_cost = safe_to_int(upgrade_table[row_idx][1]) if row_idx < len(upgrade_table) else 0
                xp_gain = safe_to_int(upgrade_table_exp[row_idx][1]) if row_idx < len(upgrade_table_exp) else 0

                if account.gold < gold_cost:
                    break

                account.gold -= gold_cost
                total_gold_spent += gold_cost

                account.exppoints += xp_gain
                total_xp_gained += xp_gain

                upgrade_events.append(
                    {
                        "cardName": c.name,
                        "fromLevel": from_level,
                        "toLevel": c.level,
                        "goldCost": gold_cost,
                    }
                )

                exp_to_next = safe_to_int(exp_table[account.explevel - 1][1]) if (account.explevel - 1) < len(exp_table) else 0
                if exp_to_next > 0 and account.exppoints >= exp_to_next:
                    account.exppoints -= exp_to_next
                    account.explevel += 1
                    per_level_cumulative_gold.append({"level": account.explevel, "cumulativeGold": total_gold_spent})

                card_data = sorted(card_data, key=lambda x: x.level)

            next_req_exp = safe_to_int(exp_table[account.explevel - 1][1]) if (account.explevel - 1) < len(exp_table) else 0
            progress_pct = 0.0
            if next_req_exp > 0:
                progress_pct = min(100.0, round((account.exppoints / next_req_exp) * 100.0, 2))

            results = {
                "playerName": player_data.get("name", ""),
                "trophies": player_data.get("trophies", 0),
                "currentLevel": player_data.get("expLevel", 0),
                "currentExp": player_data.get("expPoints", 0),
                "maxAchievableLevel": account.explevel,
                "totalExpGained": total_xp_gained,
                "totalGoldCost": total_gold_spent,
                "goldRemaining": account.gold,
                "nextLevelExpRequired": next_req_exp,
                "expTowardsNext": account.exppoints,
                "expProgressPercent": progress_pct,
                "upgradesPerformed": upgrades_performed,
                "perLevelCumulativeGold": per_level_cumulative_gold,
                "upgradeEvents": upgrade_events,
            }

            current_level = safe_to_int(player_data.get("expLevel", 0))
            current_exp = safe_to_int(player_data.get("expPoints", 0))
            current_next_req = safe_to_int(exp_table[current_level - 1][1]) if (current_level - 1) < len(exp_table) else 0
            current_pct = 0.0
            if current_next_req > 0:
                current_pct = min(100.0, round((current_exp / current_next_req) * 100.0, 2))
            results.update(
                {
                    "currentNextLevelExpRequired": current_next_req,
                    "currentExpTowardsNext": current_exp,
                    "currentExpProgressPercent": current_pct,
                }
            )
            self.root.after(0, lambda: self._render_results(results))
        except Exception as e:
            self.root.after(0, self._render_error, str(e))

    def _render_error(self, msg: str) -> None:
        self.run_btn.configure(state="normal")
        self.result_title_var.set("Calculation failed")
        self.progress_var.set(0.0)
        self.progress_text_var.set(msg)
        messagebox.showerror("Calculation Error", msg)

    def _render_results(self, r: dict) -> None:
        self.run_btn.configure(state="normal")
        self.last_results = r
        self.last_upgrade_events = r.get("upgradeEvents") or []

        self.player_line_var.set(
            f"{r.get('playerName','')}  •  Trophies: {int(r.get('trophies',0)):,}  •  King Level: {int(r.get('currentLevel',0))}"
        )
        self.current_progress_var.set(float(r.get("currentExpProgressPercent", 0.0)))
        self.current_progress_text_var.set(
            f"{int(r.get('currentExpTowardsNext', 0)):,} / {int(r.get('currentNextLevelExpRequired', 0)):,} ({r.get('currentExpProgressPercent', 0)}%)"
        )

        self.result_title_var.set(
            f"Max King Level: {r['maxAchievableLevel']}  (started at {r['currentLevel']})"
        )
        self.progress_var.set(r.get("expProgressPercent", 0.0))
        self.progress_text_var.set(
            f"Progress to next level: {r.get('expTowardsNext', 0):,} / {r.get('nextLevelExpRequired', 0):,}"
        )

        self.stats_vars["max_level"].set(str(r["maxAchievableLevel"]))
        self.stats_vars["gold_spent"].set(f"{r['totalGoldCost']:,}")
        self.stats_vars["gold_remaining"].set(f"{r['goldRemaining']:,}")
        self.stats_vars["xp_gained"].set(f"{r['totalExpGained']:,}")
        self.stats_vars["upgrades"].set(str(r["upgradesPerformed"]))

        self._render_details()


def main() -> None:
    root = tk.Tk()
    app = ClashRoyaleCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

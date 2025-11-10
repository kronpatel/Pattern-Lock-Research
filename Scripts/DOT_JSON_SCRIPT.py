import json
import os

# Android skip rules (midpoints)
skip = {
    (1, 3): 2, (3, 1): 2,
    (4, 6): 5, (6, 4): 5,
    (7, 9): 8, (9, 7): 8,
    (1, 7): 4, (7, 1): 4,
    (2, 8): 5, (8, 2): 5,
    (3, 9): 6, (9, 3): 6,
    (1, 9): 5, (9, 1): 5,
    (3, 7): 5, (7, 3): 5
}

def is_valid_move(path, nxt):
    """Check Android skip rules for valid moves."""
    if nxt in path:
        return False
    if not path:
        return True
    last = path[-1]
    mid = skip.get((last, nxt))
    if mid is None:
        return True
    return mid in path

def generate_patterns(length):
    """Generate all valid Android patterns of a given length."""
    results = []
    def backtrack(path):
        if len(path) == length:
            results.append(path.copy())
            return
        for nxt in range(1, 10):
            if is_valid_move(path, nxt):
                path.append(nxt)
                backtrack(path)
                path.pop()
    backtrack([])
    return results

# --- USER INPUT SECTION ---
while True:
    try:
        user_len = int(input("🔹 Enter number of dots (4–9): "))
        if user_len < 4:
            print("❌ Invalid input! Android requires at least 4 dots.")
            continue
        elif user_len > 9:
            print("❌ Only 9 dots max allowed.")
            continue
        else:
            break
    except ValueError:
        print("⚠️ Please enter a valid number between 4 and 9.")

# --- GENERATE & SAVE ---
print(f"\n🔹 Generating valid {user_len}-dot Android patterns...")

patterns = generate_patterns(user_len)
grouped = {str(i): [] for i in range(1, 10)}

for p in patterns:
    grouped[str(p[0])].append(''.join(map(str, p)))

folder = f"{user_len}_DOT"
os.makedirs(folder, exist_ok=True)

for start_dot, pats in grouped.items():
    data = {"count": len(pats), "patterns": pats}
    filename = os.path.join(folder, f"patterns_start_{start_dot}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {filename} ({len(pats)} patterns)")

print(f"\n🎯 Done! All {user_len}-dot JSON files saved inside '{folder}' folder.")

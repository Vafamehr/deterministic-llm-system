# --- String cleanup ---
text = "   Contract A   "
clean = text.strip().lower()
print(clean)

# --- f-string formatting ---
task = "deadline extraction"
doc = "Contract A"
msg = f"Working on {task} for {doc}"
print(msg)

# --- Safe dictionary access ---
data = {"domain": "law"}
domain = data.get("domain", "unknown")
print(domain)

# --- Simple validation ---
def process_amount(x):
    if not isinstance(x, (int, float)):
        raise ValueError("Amount must be numeric")
    return round(x, 2)

print(process_amount(10.456))

# --- Joining clean output ---
items = ["deadlines", "payment", "termination"]
summary = ", ".join(items)
print(summary)


print(all([True, True, False]))
print(any([False, True, True]))






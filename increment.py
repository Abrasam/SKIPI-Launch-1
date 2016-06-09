data = 0
with open("count.txt", "r") as f:
    try:
        data = int(f.readline())
    except Exception:
        print("Oranges!")
data+=1
with open("count.txt", "w") as f:
    try:
        f.write(str(data))
    finally:
        print("Done!")

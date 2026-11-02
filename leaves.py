leaves = []

def apply_leave(name, days, reason):
    if days <= 0:
        return "Invalid leave days"

    leave = {
        "name": name,
        "days": days,
        "reason": reason,
        "status": "Pending"
    }

    leaves.append(leave)
    return "Leave applied successfully"


def view_leaves():
    return leaves


def update_status(index, status):
    if index < 0 or index >= len(leaves):
        return "Invalid leave index"

    if status not in ["Approved", "Rejected"]:
        return "Invalid status"

    leaves[index]["status"] = status
    return "Status updated successfully"


# Main program
apply_leave("Mahek", 2, "Fever")

print("All Leave Requests:")
print(view_leaves())

update_status(0, "Approved")

print("Updated Requests:")
print(view_leaves())

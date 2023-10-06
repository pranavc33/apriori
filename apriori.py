# Function to generate C1 (candidate item sets of size 1)
def generate_C1(dataset):
    C1 = []
    for transaction in dataset:
        for item in transaction:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))

# Function to calculate support for item sets in Ck


def calculate_support(dataset, itemset, min_support):
    item_count = {}
    for transaction in dataset:
        for item in itemset:
            if item.issubset(transaction):
                item_count[item] = item_count.get(item, 0) + 1

    num_transactions = len(dataset)
    frequent_itemset = []
    support_data = {}

    for item, count in item_count.items():
        support = count / num_transactions
        if support >= min_support:
            frequent_itemset.insert(0, item)
        support_data[item] = support

    return frequent_itemset, support_data

# Function to generate Lk from Ck


def generate_Lk(dataset, candidate_set, min_support):
    itemset_count = {}
    for transaction in dataset:
        for item in candidate_set:
            if item.issubset(transaction):
                itemset_count[item] = itemset_count.get(item, 0) + 1

    num_transactions = len(dataset)
    frequent_itemset = []
    support_data = {}

    for item, count in itemset_count.items():
        support = count / num_transactions
        if support >= min_support:
            frequent_itemset.append(item)
        support_data[item] = support

    return frequent_itemset, support_data

# Function to generate Ck+1 from Lk


def generate_Ck(Lk, k):
    Ckplus1 = []
    for i in range(len(Lk)):
        for j in range(i+1, len(Lk)):
            item1 = list(Lk[i])[:k-2]
            item2 = list(Lk[j])[:k-2]
            item1.sort()
            item2.sort()
            if item1 == item2:
                Ckplus1.append(Lk[i] | Lk[j])
    return Ckplus1

# Main Apriori algorithm


def apriori(dataset, min_support):
    C1 = generate_C1(dataset)
    D = list(map(set, dataset))
    L1, support_data = calculate_support(D, C1, min_support)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        Ck = generate_Ck(L[k-2], k)
        Lk, supK = generate_Lk(D, Ck, min_support)
        support_data.update(supK)
        L.append(Lk)
        k += 1
    return L, support_data


# Get user input for transactions and minimum support
transactions = []
num_transactions = int(input("Enter the number of transactions: "))
for i in range(num_transactions):
    transaction = input(
        f"Enter items for transaction {i + 1} (comma-separated): ").split(',')
    transactions.append([item.strip() for item in transaction])

min_support = float(input("Enter the minimum support (e.g., 0.5 for 50%): "))

# Find frequent itemsets using Apriori
L, support_data = apriori(transactions, min_support)

# Display frequent itemsets
print("\nFrequent Item Sets:")
for k, itemset_list in enumerate(L):
    if k == 0:
        continue  # Skip size-0 itemsets
    print(f"Size-{k} Itemsets:")
    if itemset_list:
        for itemset in itemset_list:
            print(", ".join(item for item in itemset))

# Display support data
print("\nSupport Data:")
for item, support in support_data.items():
    print(f"{item}: {support:.2%}")

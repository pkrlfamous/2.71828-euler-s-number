principal = 1 # initial amount of money or capital
batch = 100000000 # number of times interest is applied (higher = more frequent compunding)
interest = 1/batch # interest rate per batch ( total interest =1, splitting across batches)
# loop through each batch to apply compund interest.
for i in range(batch):
    principal += interest*principal

print(f"Your principle at the end of the term with the batch {batch} is {principal}")
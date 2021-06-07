import math
import graph
import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# generate random dataset
def generate_euclidean_node(node_number):
    file_name = "test" + str(node_number) + ".txt"
    f = open(file_name, "w")
    for i in range(node_number):
        x = random.randint(0,200)
        y = random.randint(0,200)
        line = (str(x) + " " + str(y) + "\n")
        f.write(line)
    f.close()

    return file_name


def generate_metric_setting(node_number):
    file_name = "test" + str(node_number) + ".txt"
    f = open(file_name, "w")
    for i in range(node_number):
        for j in range(i+1, node_number):
            distance = random.randint(1,21)
            line = (str(i) + " " + str(j) + " " + str(distance) + "\n")
            f.write(line)
    f.close()
    return file_name

# method for permutation
def direct_enumeration(lst):
    if len(lst) == 0:
        return []

    if len(lst) == 1:
        return [lst]

    return_lst = []

    for i in range(len(lst)):
        m = lst[i]

        remain_lst = lst[:i] + lst[i+1:]

        for p in direct_enumeration(remain_lst):
            return_lst.append([m] + p)
    return return_lst



#calculate the optimal solution for 100 times and average them for node 5 to 9
def test_5_to_9_nodes():

    # initilisation
    optimal_solution = []
    christofides_solution = []
    swap_solution = []
    two_opt_solution = []
    greedy_solution = []

    optimal_total = 0
    christofides_total = 0
    swap_total = 0
    two_opt_total = 0
    greedy_total = 0

    for i in range(5, 10):
        lst = [i for i in range(i)]
        enumerate_list = direct_enumeration(lst)
        for j in range(100):
            file_name = generate_euclidean_node(i)


            optimal_len = math.inf
            optimal = graph.Graph(-1, file_name)
            for lst in enumerate_list:
                optimal.perm = lst
                if (optimal.tourValue() < optimal_len):
                    optimal_len = optimal.tourValue()
            optimal_total += optimal_len


            christofides = graph.Graph(-1, file_name)
            christofides.Christofides()
            christofides_total += christofides.tourValue()

            swap = graph.Graph(-1, file_name)
            swap.swapHeuristic(swap.n)
            swap_total += swap.tourValue()

            two_opt = graph.Graph(-1, file_name)
            two_opt.TwoOptHeuristic(two_opt.n)
            two_opt_total += two_opt.tourValue()

            greedy = graph.Graph(-1, file_name)
            greedy.Greedy()
            greedy_total += greedy.tourValue()


        # average the distance we get for 100 dataset we generate
        optimal_solution.append(optimal_total / 100)
        christofides_solution.append(christofides_total / 100)
        swap_solution.append(swap_total / 100)
        two_opt_solution.append(two_opt_total / 100)
        greedy_solution.append(greedy_total / 100)


    solution_collection = []
    solution_collection.append(optimal_solution)
    solution_collection.append(christofides_solution)
    solution_collection.append(swap_solution)
    solution_collection.append(two_opt_solution)
    solution_collection.append(greedy_solution)

    colomn_name = ["5 nodes", "6 nodes", "7 nodes", "8 nodes", "9 nodes"]
    row_name = ["optimal solution", "Christofides Heuristic", "Sawp Heuristic","2-Opt Heuristic","Greedy"]

    collection = pd.DataFrame(columns=colomn_name, index = row_name, data=solution_collection)
    collection.T.to_csv('collection.csv', encoding='utf-8')


    solution_9_nodes = [optimal_solution[4], christofides_solution[4], swap_solution[4],
                        two_opt_solution[4], greedy_solution[4]]

    print("When nodes = 9,")
    print("tour value of optimal solution is: %.0f " % solution_9_nodes[0])

    print("tour value of christofides heuristic is: %.0f " % solution_9_nodes[1],
          " difference between optimal is: {:.2%} ".format(solution_9_nodes[1] / solution_9_nodes[0] -1))

    print("tour value of swap heuristic is: %.0f " % solution_9_nodes[2],
          " difference between optimal is: {:.2%} ".format(solution_9_nodes[2] / solution_9_nodes[0] - 1))

    print("tour value of 2-Opt heuristic is: %.0f " % solution_9_nodes[3],
          " difference between optimal is: {:.2%} ".format(solution_9_nodes[3] / solution_9_nodes[0] - 1))

    print("tour value of greedy heuristic is: %.0f " % solution_9_nodes[4],
          " difference between optimal is: {:.2%}".format(solution_9_nodes[4] / solution_9_nodes[0] - 1))

    print("\n")

    return


# call this to generate data
# for comparing optimal solution using permutation,
# Christofides algorithm, Swap Heuristic, 2-opt heuristic
# and Greedy Search
# only need for once, running need about one minute.
test_5_to_9_nodes()


# generate the figure of the data above
def show_small_nodes_testing():
    solution = pd.read_csv("collection.csv")
    ax = sns.lineplot(data=solution)
    ax.set_xticks(range(len(solution)))
    ax.set_xticklabels(['5', '6', '7', '8', '9'])
    plt.xlabel('number of nodes', fontsize=16)
    plt.ylabel('Tour Value', fontsize=16)
    plt.title("Tour value for node number from 5 to 9", fontsize=18)
    ax.figure.savefig("5_to_9_nodes.png")
    plt.show()

    return

# show the plot of the comparision
show_small_nodes_testing()




# test of a dataset for different heuristic with a given optimal solution: 2579
def a280_test():
    christofides = graph.Graph(-1, "a280.txt")
    swap = graph.Graph(-1,"a280.txt")
    two_opt = graph.Graph(-1, "a280.txt")
    greedy = graph.Graph(-1, "a280.txt")

    optimal_solution = 2579
    solution_list = []
    solution_list.append(optimal_solution)

    christofides.Christofides()
    solution_list.append(christofides.tourValue())

    swap.swapHeuristic(swap.n)
    solution_list.append(swap.tourValue())

    two_opt.TwoOptHeuristic(two_opt.n)
    solution_list.append(two_opt.tourValue())

    greedy.Greedy()
    solution_list.append(greedy.tourValue())

    dataset = pd.DataFrame(columns=["Distance"], index=["Optimal", "Christofides Heuristic", "Swap Heuristic",
                                "2-Opt Heuristic", "Greedy Heuristic"], data=solution_list)
    dataset.T.to_csv('a280_result.csv', encoding='utf-8')

    print("In the second experiment for A280")

    print("tour value of optimal solution is: %.0f " % solution_list[0])

    print("tour value of christofides heuristic is: %.0f " % solution_list[1],
          " difference between optimal is: {:.2%} ".format(solution_list[1] / solution_list[0] - 1))

    print("tour value of swap heuristic is: %.0f " % solution_list[2],
          " difference between optimal is: {:.2%} ".format(solution_list[2] / solution_list[0] - 1))

    print("tour value of 2-Opt heuristic is: %.0f " % solution_list[3],
          " difference between optimal is: {:.2%} ".format(solution_list[3] / solution_list[0] - 1))

    print("tour value of greedy heuristic is: %.0f " % solution_list[4],
          " difference between optimal is: {:.2%}".format(solution_list[4] / solution_list[0] - 1))

    print("\n")

    return



def att48_test():
    christofides = graph.Graph(-1, "att48_xy.txt")
    swap = graph.Graph(-1,"att48_xy.txt")
    two_opt = graph.Graph(-1, "att48_xy.txt")
    greedy = graph.Graph(-1, "att48_xy.txt")

    optimal_solution = 33523
    solution_list = []
    solution_list.append(optimal_solution)

    christofides.Christofides()
    solution_list.append(christofides.tourValue())

    swap.swapHeuristic(swap.n)
    solution_list.append(swap.tourValue())

    two_opt.TwoOptHeuristic(two_opt.n)
    solution_list.append(two_opt.tourValue())

    greedy.Greedy()
    solution_list.append(greedy.tourValue())

    dataset = pd.DataFrame(columns=["Distance"], index=["Optimal", "Christofides Heuristic", "Swap Heuristic", "2-Opt Heuristic",
                                    "Greedy Heuristic"], data=solution_list)

    dataset.T.to_csv('att48_result.csv', encoding='utf-8')

    print("In the third experiment for ATT48")

    print("tour value of optimal solution is: %.0f " % solution_list[0])

    print("tour value of christofides heuristic is: %.0f " % solution_list[1],
          " difference between optimal is: {:.2%} ".format(solution_list[1] / solution_list[0] -1))

    print("tour value of swap heuristic is: %.0f " % solution_list[2],
          " difference between optimal is: {:.2%} ".format(solution_list[2] / solution_list[0] - 1))

    print("tour value of 2-Opt heuristic is: %.0f " % solution_list[3],
          " difference between optimal is: {:.2%} ".format(solution_list[3] / solution_list[0] - 1))

    print("tour value of greedy heuristic is: %.0f " % solution_list[4],
          " difference between optimal is: {:.2%}".format(solution_list[4] / solution_list[0] - 1))

    print("\n")

    return


# These two method are calculating the tour value after implementing different heuristic and save the data
# as dataframe.  Only need to execute once.
a280_test()
att48_test()


# plot the bar chart of the data we get for dataset a280
def plot_a280():
    dataset = pd.read_csv("a280_result.csv")
    plt.figure(figsize=(10, 10))
    ax = sns.barplot(data=dataset)
    plt.xlabel('methods', fontsize=16)
    plt.ylabel('Tour Value', fontsize=16)
    plt.title("Tour value for dataset a280", fontsize= 20)
    ax.set(ylim=2200)
    ax.figure.savefig("a280_result.png")
    plt.show()
    return


# plot the bar chart of the data we get for dataset att48
def plot_att48():
    dataset = pd.read_csv("att48_result.csv")
    plt.figure(figsize=(10, 10))
    ax = sns.barplot(data=dataset)
    plt.xlabel('methods', fontsize=16)
    plt.ylabel('Tour Value', fontsize=16)
    plt.title("Tour value for dataset att48", fontsize= 20)
    ax.set(ylim=22000)
    ax.figure.savefig("att48_result.png")
    plt.show()
    return

plot_a280()
plot_att48()
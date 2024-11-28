import random
from copy import deepcopy
from tabulate import tabulate


class ExecutionPlan:
    def __init__(self, plan):
        self.plan = plan  # A list of x rounds, each with y processes
        self.cost = 0  # Cost of the execution plan

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return str(self.cost)

    def print_plan(self):
        headers = [f"Processor {i + 1}" for i in range(len(self.plan[0]))]
        table = [round for round in self.plan]
        print(tabulate(self.plan, headers=headers, tablefmt="pretty", showindex=range(1, len(self.plan) + 1)))


class Optimize:

    def __init__(self):
        self.GENERATION_COUNT = 1000
        self.PROCESS_COUNT = int(input("Enter the process count: "))
        self.PROCESSOR_COUNT = int(input("Enter the processor count: "))
        self.MUTATION_COUNT = self.PROCESS_COUNT // 10

    def run(self):
        # Create 100 processes with random costs between 1 and 100
        processes = [random.randint(1, 100) for _ in range(self.PROCESS_COUNT)]

        # Generate 10 initial execution plans
        execution_plans = self.create_and_initialize_plans(processes)

        # Simulate genetic evolution for GENERATION_COUNT iterations
        for generation in range(self.GENERATION_COUNT):
            # Compute costs for each execution plan
            self.compute_cost_of_plans(execution_plans)

            # Sort plans by cost (ascending order)
            execution_plans.sort()

            # Print costs of all plans
            print(f"{generation+1} = {[str(plan) for plan in execution_plans]}")

            # Clone the top 5 plans over the bottom 5 plans(“survival of the fittest”)
            self.clone_better_plans_over_worse_plans(execution_plans)

            # Mutate the cloned plans to introduce diversity
            self.mutate_clones(execution_plans)
        print(f'\nThe best plan received after {self.GENERATION_COUNT} generations is:')
        execution_plans[0].print_plan()
        print(f'The cost of the plan is: {execution_plans[0]}')

    def create_and_initialize_plans(self, processes):
        execution_plans = []
        for _ in range(10):
            random.shuffle(processes)
            plan = [processes[i:i + self.PROCESSOR_COUNT] for i in range(0, self.PROCESS_COUNT, self.PROCESSOR_COUNT)]
            execution_plans.append(ExecutionPlan(plan))
        return execution_plans

    def compute_cost_of_plans(self, execution_plans):
        for plan in execution_plans:    # we have total 10 execution plans
            plan.cost = 0
            for round in plan.plan:     # We pick up the first plan and iterate over all of its rounds(25 if 100pro/4pr)
                # Cost of a round is the maximum value (communication time) in the round
                plan.cost += max(round)

    def clone_better_plans_over_worse_plans(self, execution_plans):
        for i in range(len(execution_plans) // 2):
            clone_plan = deepcopy(execution_plans[i].plan)
            execution_plans[len(execution_plans) // 2 + i] = ExecutionPlan(clone_plan)  # now initial cost is reset to 0

    def mutate_clones(self, execution_plans):
        for i in range(len(execution_plans) // 2):
            plan = execution_plans[i]
            for _ in range(self.MUTATION_COUNT):
                loc1 = random.randint(0, self.PROCESS_COUNT-1)
                loc2 = random.randint(0, self.PROCESS_COUNT-1)
                r1, c1 = divmod(loc1, self.PROCESSOR_COUNT)
                r2, c2 = divmod(loc2, self.PROCESSOR_COUNT)
                # Swap two processes in the plan
                plan.plan[r1][c1], plan.plan[r2][c2] = plan.plan[r2][c2], plan.plan[r1][c1]


if __name__ == "__main__":
    optimizer = Optimize()
    optimizer.run()

import matplotlib.pyplot    as plt
from collections            import deque
import random

class OpticalNetworkSimulation:
    
    def __init__(self, num_slots, pcs_count = 8):
        self.server = "Server"
        pcs = []
        for i in range(pcs_count):
            pcs.append(f"PC{i + 1}") # PC1, PC2, ..., PC8

        # each PC has its own queue (fifo)
        self.pcs = {}
        for pc in pcs:
            self.pcs[pc] = deque()

        group1 = ["PC1", "PC2"]
        group2 = ["PC3", "PC4"]
        group3 = ["PC5", "PC6"]
        group4 = ["PC7", "PC8"]
        self.wavelengths = {
            1: group1,
            2: group2,
            3: group3,
            4: group4}
        
        # initialize queues for each wavelength
        self.slot_queue = {}
        for wavelength in self.wavelengths:
            self.slot_queue[wavelength] = []

        self.num_slots = num_slots # time slots
        self.total_packets_sent = 0 # total successfully sent packets
        self.total_delay = 0 # total delay of sent packets
        self.total_packets_created = 0 # total packets generated
        self.total_packets_lost = 0 # total packets dropped due to queue overflow

    # Generate packets with a given probability
    def generate_packet_arrivals(self, arrival_probability, current_time):
        for _, queue in self.pcs.items():
            if random.random() < arrival_probability:  # probability of packet arrival
                self.total_packets_created += 1
                packet = {"arrival_time": current_time, "data": f"Packet-{random.randint(1, 100)}"}
                if len(queue) < 5:  # queue capacity (max: 5)
                    queue.append(packet)
                else:
                    self.total_packets_lost += 1  # packet dropped because of full queue

    # schedule packets for transmission
    def schedule_packets(self):        
        for pc, queue in self.pcs.items():
            if queue and random.random() < 0.5:  # 0.5: transmission probability
                for w, pcs in self.wavelengths.items():
                    if pc in pcs:
                        data = queue.popleft()  # dequeue packet
                        self.slot_queue[w].append((pc, self.server, data))
                        break

    # handle collisions and calculate delays
    def handle_collisions(self, current_time):
        for wavelength, transmissions in self.slot_queue.items():
            if len(transmissions) > 1:  # collision detected
                for sender, _, packet in transmissions:
                    self.pcs[sender].appendleft(packet)  # return packet to sender's queue
            elif len(transmissions) == 1: # successful transmission
                sender, _, packet = transmissions[0]
                self.total_packets_sent += 1
                delay = current_time - packet["arrival_time"] + 1  # delay calculation
                self.total_delay += delay
            self.slot_queue[wavelength] = []

    def run_simulation(self, arrival_probability):
        self.total_packets_sent = 0
        self.total_delay = 0
        self.total_packets_created = 0
        self.total_packets_lost = 0
        for slot in range(self.num_slots):
            self.generate_packet_arrivals(arrival_probability, current_time = slot)
            self.schedule_packets() # transmit packets probabilistically
            self.handle_collisions(current_time = slot) # detecting and returning collided packets to their queues

        throughput = self.total_packets_sent / self.num_slots
        if self.total_packets_sent > 0:
            avg_delay = self.total_delay / self.total_packets_sent
        else:
            avg_delay = 0

        if self.total_packets_created > 0:
            loss_rate = self.total_packets_lost / self.total_packets_created
        else:
            loss_rate = 0

        return throughput, avg_delay, loss_rate

NUM_SLOTS = int(input("Enter how many time slots: "))
while NUM_SLOTS < 0:
    NUM_SLOTS = int(input("Enter how many time slots (positive number): "))
print(f"Calculating throughputs, average packet delay and loss rates for {NUM_SLOTS} time slots...")
print("Plotting results...")
pcs_count = 8 # computers (pc1, pc2, ..., pc8)
probabilities = []
for i in range(1, 11):
    probabilities.append(i / 10) # P = 0.1, 0.2, ..., 1.0

# Results variables/lists
throughputs = []
average_delays = []
loss_rates = []

# for each arrival probability:
for p in probabilities:
    network = OpticalNetworkSimulation(num_slots=NUM_SLOTS, pcs_count=pcs_count)
    throughput, avg_delay, loss_rate = network.run_simulation(arrival_probability=p)
    throughputs.append(throughput)
    average_delays.append(avg_delay)
    loss_rates.append(loss_rate)

"""Plotting the results"""

# Throughput
plt.figure(num = 1, figsize = (10, 6))
plt.plot(probabilities, throughputs, marker = "o", label = "Throughput")
plt.title("Throughput")
plt.xlabel("Packet Arrival Probability (P)")
plt.ylabel("Throughput")
plt.grid()
plt.legend()

# Average Packet Delay
plt.figure(num = 2, figsize = (10, 6))
plt.plot(probabilities, average_delays, marker = "o", label = "Average Packet Delay", color = "orange")
plt.title("Average Packet Delay")
plt.xlabel("Packet Arrival Probability (P)")
plt.ylabel("Average Packet Delay (in Slots)")
plt.grid()
plt.legend()

# Packet Loss Rate
plt.figure(num = 3, figsize = (10, 6))
plt.plot(probabilities, loss_rates, marker = "o", label = "Packet Loss Rate", color = "red")
plt.title("Packet Loss Rate")
plt.xlabel("Packet Arrival Probability (P)")
plt.ylabel("Packet Loss Rate")
plt.grid()
plt.legend()

plt.show()

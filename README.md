# Optical-Communications-Project
Optical Communications Project: A simple optical network simulation in python

This optical network simulation implementation in python, presents an optical network with 8 computers using 4 wavelengths (λ1-λ4) to send packets to a server via WDM multiplexer. The time is divided into slots, with each computer having a queue with a capacity of 5 packages. If the queue is full, new packages are lost. Transmissions occur with a success probability of 0.5, while collision occurs when two stations share the same wavelength and broadcast on the same slot. Conflicting packets remain in queues for rebroadcast.

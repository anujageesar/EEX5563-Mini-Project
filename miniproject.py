import tkinter as tk
from tkinter import messagebox


class WorstFitMemoryAllocator:
    def __init__(self, memory_blocks):
        self.memory_blocks = sorted(memory_blocks, reverse=True)

    def allocate(self, request_size):
        for i, block in enumerate(self.memory_blocks):
            if block >= request_size:
                allocated = self.memory_blocks.pop(i)
                remaining = allocated - request_size
                if remaining > 0:
                    self.memory_blocks.append(remaining)
                    self.memory_blocks.sort(reverse=True)
                return f"Allocated {request_size} units. Remaining blocks: {self.memory_blocks}"
        return f"Request for {request_size} units denied. No suitable block available."

    def deallocate(self, block_size):
        self.memory_blocks.append(block_size)
        self.memory_blocks.sort(reverse=True)
        return f"Deallocated {block_size} units. Available blocks: {self.memory_blocks}"

    def display_memory_blocks(self):
        return f"Current memory blocks: {self.memory_blocks}"


class MemoryAllocatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Worst Fit Memory Allocator")
        self.allocator = None

        # Input for Initial Memory Blocks
        tk.Label(root, text="Enter Initial Memory Blocks (comma-separated):").pack(pady=5)
        self.memory_input = tk.Entry(root, width=30)
        self.memory_input.pack(pady=5)

        # Button to Initialize Allocator
        tk.Button(root, text="Initialize Allocator", command=self.initialize_allocator).pack(pady=5)

        # Output Display
        self.output_label = tk.Label(root, text="", wraplength=400, justify="left")
        self.output_label.pack(pady=10)

        # Operation Frame
        self.operation_frame = tk.Frame(root)
        self.operation_frame.pack(pady=10)

        # Input for Allocation/Deallocation
        tk.Label(self.operation_frame, text="Enter Memory Size:").grid(row=0, column=0, padx=5, pady=5)
        self.size_input = tk.Entry(self.operation_frame, width=10)
        self.size_input.grid(row=0, column=1, padx=5, pady=5)

        # Buttons for Operations
        tk.Button(self.operation_frame, text="Allocate", command=self.allocate_memory).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.operation_frame, text="Deallocate", command=self.deallocate_memory).grid(row=1, column=1, padx=5, pady=5)

        # Button to Display Current Memory Blocks
        tk.Button(root, text="Display Memory Blocks", command=self.display_memory).pack(pady=5)

    def initialize_allocator(self):
        try:
            memory_blocks = list(map(int, self.memory_input.get().strip().split(',')))
            self.allocator = WorstFitMemoryAllocator(memory_blocks)
            self.output_label.config(text="Allocator initialized successfully.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    def allocate_memory(self):
        if self.allocator:
            try:
                request_size = int(self.size_input.get().strip())
                result = self.allocator.allocate(request_size)
                self.output_label.config(text=result)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid memory size.")
        else:
            messagebox.showwarning("Initialization Error", "Please initialize the allocator first.")

    def deallocate_memory(self):
        if self.allocator:
            try:
                block_size = int(self.size_input.get().strip())
                result = self.allocator.deallocate(block_size)
                self.output_label.config(text=result)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid memory size.")
        else:
            messagebox.showwarning("Initialization Error", "Please initialize the allocator first.")

    def display_memory(self):
        if self.allocator:
            result = self.allocator.display_memory_blocks()
            self.output_label.config(text=result)
        else:
            messagebox.showwarning("Initialization Error", "Please initialize the allocator first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocatorApp(root)
    root.mainloop()

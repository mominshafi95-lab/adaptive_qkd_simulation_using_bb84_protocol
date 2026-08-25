import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path
import numpy as np

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.bb84_engine import BB84Engine

class BB84GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive BB84 QKD Simulator")
        self.root.geometry("600x700")
        
        # Title
        title_label = tk.Label(root, text="Adaptive BB84 QKD Simulator", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Input Frame
        input_frame = ttk.LabelFrame(root, text="Parameters", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Noise Probability
        tk.Label(input_frame, text="Noise Probability (0.0-1.0):").pack(anchor="w")
        self.noise_entry = tk.Entry(input_frame, width=30)
        self.noise_entry.insert(0, "0.05")
        self.noise_entry.pack(anchor="w", pady=5)
        
        # Run Button
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.run_button = tk.Button(button_frame, text="Run QKD Protocol", command=self.run_qkd, 
                                     bg="green", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        self.run_button.pack(side="left", padx=5)
        
        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_output,
                                       bg="gray", fg="white", font=("Arial", 10), padx=15, pady=5)
        self.clear_button.pack(side="left", padx=5)
        
        # Output Frame
        output_frame = ttk.LabelFrame(root, text="Results", padding=10)
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(output_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Output Text
        self.output_text = tk.Text(output_frame, height=20, width=60, yscrollcommand=scrollbar.set)
        self.output_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.output_text.yview)
        
        # Status Bar
        self.status_label = tk.Label(root, text="Ready", relief="sunken", anchor="w", bg="lightgray")
        self.status_label.pack(side="bottom", fill="x")
    
    def run_qkd(self):
        try:
            self.status_label.config(text="Running QKD protocol...")
            self.root.update()
            
            noise_prob = float(self.noise_entry.get())
            if not (0.0 <= noise_prob <= 1.0):
                self.output_text.insert(tk.END, "Error: Noise probability must be between 0.0 and 1.0\n")
                self.status_label.config(text="Error: Invalid input")
                return
            
            engine = BB84Engine(16, noise_prob=noise_prob)
            result = engine.run()
            
            # Clear and display results
            self.output_text.delete("1.0", tk.END)
            
            if 'qber' not in result:
                self.output_text.insert(tk.END, "Error: QKD protocol failed to generate sifted key\n")
                self.status_label.config(text="Error: QKD failed")
                return
            
            output = f"""
RESULTS
{'='*50}

Protocol Status:       {'SECURE' if result['secure'] else 'INSECURE'}

Quantum Transmission:
  - Sifted Key Length: {result['sifted_length']} bits
  - Detection Bit:     QBER (Quantum Bit Error Rate)
  
QBER Analysis:
  - Raw QBER:          {result['qber']:.4f}
  - Adjusted QBER:     {result['adjusted_qber']:.4f}
  - QBER Threshold:    0.1100
  
Information Theory:
  - I(A:B):            {result['I_AB']:.4f} bits
  - I(A:E):            {result['I_AE']:.4f} bits
  - Advantage:         {result['I_AB'] - result['I_AE']:.4f} bits
  
Final Results:
  - Final Key Length:  {result['final_key_length']} bits
  - Error Leakage:     {result['leakage']} bits
  - Decoy State Used:  {result['decoy_used']}
  
{'='*50}
"""
            self.output_text.insert(tk.END, output)
            
            if result['secure']:
                self.status_label.config(text="Protocol completed - KEY IS SECURE")
            else:
                reason = []
                if result['adjusted_qber'] > 0.11:
                    reason.append(f"QBER too high ({result['adjusted_qber']:.4f} > 0.11)")
                if result['I_AB'] <= result['I_AE']:
                    reason.append("Eve has more information than legitimate users")
                self.status_label.config(text=f"Protocol completed - INSECURE: {'; '.join(reason)}")
            
        except ValueError:
            self.output_text.insert(tk.END, "Error: Invalid noise probability value. Please enter a number.\n")
            self.status_label.config(text="Error: Invalid input")
        except Exception as e:
            error_msg = f"Error: {str(e)}\n"
            self.output_text.insert(tk.END, error_msg)
            self.status_label.config(text="Error")
    
    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self.status_label.config(text="Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = BB84GUI(root)
    root.mainloop()

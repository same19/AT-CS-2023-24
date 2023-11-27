print("\nHello world\n")
import numpy as np
print()
a = np.abs(np.fft.rfft(np.sin(range(100))))
print(np.fft.rfftfreq(100)[np.max(a)])
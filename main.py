import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QListWidget, QLineEdit, QTextEdit, QPushButton, QLabel, 
                            QListWidgetItem, QFileDialog, QProgressBar, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QTextCursor
import mpmath as mp
from mpmath import workprec, iv

mp.dps = 100  # Initial precision

# ======================================================================
# Calculation Worker Thread
# ======================================================================

class CalculationThread(QThread):
    update_progress = pyqtSignal(int, str)
    result_ready = pyqtSignal(str, str)

    def __init__(self, constant_data, precision):
        super().__init__()
        self.constant_data = constant_data
        self.precision = precision
        self._is_running = True

    def run(self):
        try:
            result = ""
            formula = ""
            with workprec(int(self.precision * 1.1)):
                for progress in self._simulate_calculation():
                    if not self._is_running:
                        return
                    self.update_progress.emit(progress, self.constant_data['formula'])
                
                value = self.constant_data['func']()
                result = mp.nstr(value, self.precision) if isinstance(value, (mp.mpf, iv.mpf)) else str(value)
                formula = self.constant_data['formula']
            
            self.result_ready.emit(result, formula)
        except Exception as e:
            self.result_ready.emit(f"⨯ Error: {str(e)}", "")

    def _simulate_calculation(self):
        for i in range(1, 101):
            time.sleep(0.01)
            yield i

    def stop(self):
        self._is_running = False

# ======================================================================
# Main Application Window
# ======================================================================

class ConstantsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.constants = self._load_constants()
        self.init_ui()
        self.current_constant = None
        self.calculation_thread = None


    def _load_constants(self):
        return {
    # Mathematical Constants (1-45)
    "Pi": {
        'func': lambda: mp.pi,
        'formula': "π = 4∑ₖ₌₀^∞ (-1)ᵏ/(2k+1)",
        'accuracy': "Exact infinite series",
        'reference': "Archimedes' constant"
    },
    "Euler’s Number": {
        'func': lambda: mp.e,
        'formula': "e = limₙ→∞ (1 + 1/n)ⁿ",
        'accuracy': "Exact limit definition",
        'reference': "Natural logarithm base"
    },
    "Golden Ratio": {
        'func': lambda: (1 + mp.sqrt(5)) / 2,
        'formula': "ϕ = (1 + √5)/2",
        'accuracy': "Exact algebraic value",
        'reference': "Quadratic equation"
    },
    "Square Root of 2": {
        'func': lambda: mp.sqrt(2),
        'formula': "√2 = 2^(1/2)",
        'accuracy': "Exact value",
        'reference': "Pythagorean constant"
    },
    "Square Root of 3": {
        'func': lambda: mp.sqrt(3),
        'formula': "√3 = 3^(1/2)",
        'accuracy': "Exact value",
        'reference': "Theodorus' constant"
    },
    "Apéry’s Constant": {
        'func': lambda: mp.zeta(3),
        'formula': "ζ(3) = ∑ₙ₌₁^∞ 1/n³",
        'accuracy': "Series summation",
        'reference': "Apery's proof"
    },
    "Feigenbaum Delta": {
        'func': lambda: mp.findroot(lambda x: (mp.pi**2 - 6*x**2)/12 - mp.cos(x), 4.669),
        'formula': "δ = limₙ→∞ (aₙ - aₙ₋₁)/(aₙ₊₁ - aₙ)",
        'accuracy': "Numerical approximation",
        'reference': "Bifurcation theory"
    },
    "Feigenbaum Alpha": {
        'func': lambda: mp.mpf('2.502907875095892822283'),
        'formula': "α = -1/δ limₙ→∞ (gₙ(0) - gₙ₋₁(0))/(gₙ₊₁(0) - gₙ(0))",
        'accuracy': "Numerical approximation",
        'reference': "Bifurcation theory"
    },
    "Catalan’s Constant": {
        'func': lambda: mp.catalan,
        'formula': "G = ∑ₖ₌₀^∞ (-1)ᵏ/(2k+1)²",
        'accuracy': "Accelerated series",
        'reference': "Catalan (1883)"
    },
    "Khinchin’s Constant": {
        'func': lambda: mp.khinchin,
        'formula': "K₀ = ∏ₖ₌₁^∞ (1 + 1/k(k+2))^(log₂ k)",
        'accuracy': "Numerical integration",
        'reference': "Continued fractions"
    },
    "Glaisher–Kinkelin Constant": {
        'func': lambda: mp.glaisher,
        'formula': "A = limₙ→∞ (∏ₖ₌₁^n k^k)/(n^(n²/2 + n/2 + 1/12)e^(-n²/4))",
        'accuracy': "Hyperfactorial limit",
        'reference': "Kinkelin's theorem"
    },
    "Omega Constant": {
        'func': lambda: mp.lambertw(1),
        'formula': "Ω e^Ω = 1",
        'accuracy': "Root-finding method",
        'reference': "Lambert W function"
    },
    "Champernowne’s Constant": {
        'func': lambda: mp.champernowne(10),
        'formula': "C₁₀ = 0.12345678910111213...",
        'accuracy': "Algorithmic generation",
        'reference': "Normal number"
    },
    "Euler–Mascheroni Constant": {
        'func': lambda: mp.euler,
        'formula': "γ = limₙ→∞ (∑ₖ₌₁^n 1/k - ln n)",
        'accuracy': "Harmonic series limit",
        'reference': "Number theory"
    },
    "Conway’s Constant": {
        'func': lambda: mp.mpf('1.303577269034296'),
        'formula': "λ = Root of 71x³ - 156x² + 104x - 16 = 0",
        'accuracy': "Algebraic approximation",
        'reference': "Look-and-say sequence"
    },
    "Liouville’s Constant": {
        'func': lambda: sum(1/mp.power(10, mp.factorial(k)) for k in range(1, 10)),
        'formula': "L = ∑ₖ₌₁^∞ 10^(-k!)",
        'accuracy': "Partial summation",
        'reference': "Transcendental number"
    },
    "Laplace Limit": {
        'func': lambda: mp.mpf('1.199678640257734'),
        'formula': "ε = Root of εe^√(1+ε²)/(1+√(1+ε²)) = 1",
        'accuracy': "Numerical solution",
        'reference': "Kepler equation"
    },
    "Twin Prime Constant": {
        'func': lambda: mp.mpf('0.6601618158468695739278121'),
        'formula': "C₂ = ∏ₚ>2 (1 - 1/(p-1)²)",
        'accuracy': "Prime product approximation",
        'reference': "Hardy-Littlewood conjecture"
    },
    "Mertens’ Constant": {
        'func': lambda: mp.mertens(4),
        'formula': "B₁ = limₙ→∞ (∑ₚ≤ₙ 1/p - ln ln n)",
        'accuracy': "Prime summation",
        'reference': "Prime number theory"
    },
    "Somos’ Quadratic Recurrence Constant": {
        'func': lambda: mp.nstr(mp.somos(4), 15),
        'formula': "σ = √(1√(2√(3√(4...)))",
        'accuracy': "Nested radical calculation",
        'reference': "Recurrence relation"
    },
    "Plastic Constant": {
        'func': lambda: ((9 + mp.sqrt(69))/18)**(1/3) + ((9 - mp.sqrt(69))/18)**(1/3),
        'formula': "ρ = ∛((9+√69)/18) + ∛((9-√69)/18)",
        'accuracy': "Exact algebraic",
        'reference': "Cube root equation"
    },
    "Tetration Constant": {
        'func': lambda: mp.nstr(mp.ln(2)**(-mp.ln(2)), 15),
        'formula': "∞ = limₙ→∞ ⁿ2",
        'accuracy': "Approximation",
        'reference': "Infinite tower exponent"
    },
    "de Bruijn–Newman Constant": {
        'func': lambda: mp.mpf('0.2'),
        'formula': "Λ ≥ 0",
        'accuracy': "Current best bound",
        'reference': "Riemann hypothesis"
    },
    "Brun’s Constant": {
        'func': lambda: mp.mpf('1.902160583104'),
        'formula': "B₂ = ∑(1/p + 1/(p+2))",
        'accuracy': "Prime twin summation",
        'reference': "Twin prime conjecture"
    },
    "Prouhet–Thue-Morse Constant": {
        'func': lambda: mp.mpf('0.412454033640'),
        'formula': "τ = ∑ₙ₌₀^∞ tₙ/2^(n+1)",
        'accuracy': "Binary expansion",
        'reference': "Sequence automaton"
    },
    "Ramanujan Constant": {
        'func': lambda: mp.exp(mp.pi*mp.sqrt(163)),
        'formula': "e^(π√163)",
        'accuracy': "Almost integer",
        'reference': "Complex multiplication"
    },
    "Copeland–Erdős Constant": {
        'func': lambda: mp.champernowne(10, 0),
        'formula': "C = 0.23571113171923293137...",
        'accuracy': "Prime concatenation",
        'reference': "Prime sequence"
    },
    "Gauss’s Constant": {
        'func': lambda: 1/mp.agm(1, mp.sqrt(2)),
        'formula': "G = 1/AGM(1,√2)",
        'accuracy': "Arbitrary precision",
        'reference': "Arithmetic-geometric mean"
    },
    "Mills’ Constant": {
        'func': lambda: mp.mpf('1.306377883863080690468614'),
        'formula': "θ = limₙ→∞ Pₙ^(3^(-n))",
        'accuracy': "Prime approximation",
        'reference': "Prime-generating function"
    },
    "Dottie Number": {
        'func': lambda: mp.findroot(lambda x: mp.cos(x) - x, 0.739085),
        'formula': "ω = cos(ω)",
        'accuracy': "Fixed-point iteration",
        'reference': "Transcendental equation"
    },
    "Silver Ratio": {
        'func': lambda: 1 + mp.sqrt(2),
        'formula': "δₛ = 1 + √2",
        'accuracy': "Exact algebraic",
        'reference': "Metallic mean"
    },
    "Nested Radical Constant": {
        'func': lambda: mp.findroot(lambda x: mp.sqrt(x + x) - x, 2),
        'formula': "c = √(2 + √(2 + √(2 + ⋯))",
        'accuracy': "Infinite radical solution",
        'reference': "Recursive radical"
    },
    "Tribonacci Constant": {
        'func': lambda: (1 + (19 - 3*mp.sqrt(33))**(1/3) + (19 + 3*mp.sqrt(33))**(1/3)) / 3,
        'formula': "T = [1 + ∛(19-3√33) + ∛(19+3√33)]/3",
        'accuracy': "Exact algebraic",
        'reference': "Tribonacci sequence"
    },
    "Reciprocal Fibonacci Constant": {
        'func': lambda: mp.nsum(lambda n: 1/mp.fib(n), [1, mp.inf]),
        'formula': "ψ = ∑ₙ₌₁^∞ 1/Fₙ",
        'accuracy': "Series summation",
        'reference': "Fibonacci series"
    },
    "Lévy’s Constant": {
        'func': lambda: mp.pi**2/(12*mp.log(2)),
        'formula': "β = π²/(12 ln 2)",
        'accuracy': "Exact derivation",
        'reference': "Continued fraction theory"
    },
    "Kolmogorov Constant": {
        'func': lambda: mp.mpf('1.7'),
        'formula': "Cᴋ ≈ 1.7",
        'accuracy': "Empirical approximation",
        'reference': "Turbulence theory"
    },
    "Gelfond’s Constant": {
        'func': lambda: mp.exp(mp.pi),
        'formula': "e^π",
        'accuracy': "Exact transcendental",
        'reference': "Gelfond's theorem"
    },
    "Bailey–Borwein–Plouffe Constant": {
        'func': lambda: mp.pi,
        'formula': "π = ∑ₖ₌₀^∞ [4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)]/16ᵏ",
        'accuracy': "Exact formula",
        'reference': "BBP algorithm"
    },
    "Erdős–Borwein Constant": {
        'func': lambda: mp.nsum(lambda n: 1/(2**n - 1), [1, mp.inf]),
        'formula': "E = ∑ₙ₌₁^∞ 1/(2ⁿ - 1)",
        'accuracy': "Series summation",
        'reference': "Exponential series"
    },
    "Landau–Ramanujan Constant": {
        'func': lambda: mp.mpf('0.764223653589'),
        'formula': "K = 1/√2 ∏ₚ≡3 mod4 (1 - 1/p²)^(-1/2)",
        'accuracy': "Prime product approximation",
        'reference': "Number theory"
    },
    "Gauss–Kuzmin–Wirsing Constant": {
        'func': lambda: mp.mpf('0.303663002898'),
        'formula': "λ = limₙ→∞ [Fₙ(x) - n]/[(-1)ⁿn^(-k)]",
        'accuracy': "Continued fraction theory",
        'reference': "Operator eigenvalue"
    },
    "Sophomore’s Dream Constant": {
        'func': lambda: mp.nsum(lambda n: 1/(n**n), [1, mp.inf]),
        'formula': "S = ∑ₙ₌₁^∞ 1/nⁿ",
        'accuracy': "Series summation",
        'reference': "Johann Bernoulli"
    },
    "Somos‑6 Constant": {
        'func': lambda: mp.mpf('1.385060285204'),
        'formula': "σ₆ = √(6, √(6, √(6, ...)))",
        'accuracy': "Nested radical approximation",
        'reference': "Recurrence relation"
    },
    "Lemniscate Constant": {
        'func': lambda: mp.ellipe(0.5),
        'formula': "L = ∫₀¹ dt/√(1 - t⁴)",
        'accuracy': "Elliptic integral",
        'reference': "Lemniscate function"
    },
    "Chaitin’s Constant": {
        'func': lambda: mp.mpf('0.00787499699'),
        'formula': "Ω = ∑ₚ halts 2^(-|p|)",
        'accuracy': "Approximation",
        'reference': "Algorithmic information theory"
    },

    # Physical Constants (46-100)
    "Fine‑Structure Constant": {
        'func': lambda: mp.mpf('0.0072973525693'),
        'formula': "α = e²/(4πε₀ℏc)",
        'accuracy': "0.15 ppb",
        'reference': "CODATA 2018"
    },
    "Bohr Radius": {
        'func': lambda: mp.mpf('5.29177210903e-11'),
        'formula': "a₀ = 4πε₀ℏ²/(mₑe²)",
        'accuracy': "Exact (SI)",
        'reference': "NIST Standard"
    },
    "Rydberg Constant": {
        'func': lambda: mp.mpf('10973731.568160'),
        'formula': "R_∞ = mₑe⁴/(8ε₀²h³c)",
        'accuracy': "0.0002 cm⁻¹",
        'reference': "CODATA 2018"
    },
    "Electron Compton Wavelength": {
        'func': lambda: mp.mpf('2.42631023867e-12'),
        'formula': "λ_C = h/(mₑc)",
        'accuracy': "0.089 ppm",
        'reference': "NIST Standard"
    },
    "Planck Length": {
        'func': lambda: mp.mpf('1.616255e-35'),
        'formula': "ℓ_P = √(ℏG/c³)",
        'accuracy': "0.64 ppm",
        'reference': "CODATA 2018"
    },
    "Planck Time": {
        'func': lambda: mp.mpf('5.391247e-44'),
        'formula': "t_P = √(ℏG/c⁵)",
        'accuracy': "0.64 ppm",
        'reference': "CODATA 2018"
    },
    "Planck Mass": {
        'func': lambda: mp.mpf('2.176434e-8'),
        'formula': "m_P = √(ℏc/G)",
        'accuracy': "0.64 ppm",
        'reference': "CODATA 2018"
    },
    "Planck Temperature": {
        'func': lambda: mp.mpf('1.416784e32'),
        'formula': "T_P = m_Pc²/k_B",
        'accuracy': "0.64 ppm",
        'reference': "CODATA 2018"
    },
    "Planck Charge": {
        'func': lambda: mp.mpf('1.875545956e-18'),
        'formula': "q_P = √(4πε₀ℏc)",
        'accuracy': "Exact definition",
        'reference': "Natural units"
    },
    "Stefan–Boltzmann Constant": {
        'func': lambda: mp.mpf('5.670374419e-8'),
        'formula': "σ = 2π⁵k_B⁴/(15h³c²)",
        'accuracy': "0.035 ppm",
        'reference': "CODATA 2018"
    },
    "Magnetic Flux Quantum": {
        'func': lambda: mp.mpf('2.067833848e-15'),
        'formula': "Φ₀ = h/(2e)",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Coulomb’s Constant": {
        'func': lambda: 1/(4*mp.pi*mp.epsilon0),
        'formula': "k_e = 1/(4πε₀)",
        'accuracy': "Exact definition",
        'reference': "SI units"
    },
    "Boltzmann’s Constant": {
        'func': lambda: mp.mpf('1.380649e-23'),
        'formula': "k_B = R/N_A",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Gas Constant": {
        'func': lambda: mp.mpf('8.314462618'),
        'formula': "R = N_A k_B",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Faraday Constant": {
        'func': lambda: mp.mpf('96485.33212'),
        'formula': "F = N_A e",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Elementary Charge": {
        'func': lambda: mp.mpf('1.602176634e-19'),
        'formula': "e = 2αh/(μ₀c)",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Reduced Planck Constant": {
        'func': lambda: mp.mpf('1.054571817e-34'),
        'formula': "ℏ = h/(2π)",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Gravitational Constant": {
        'func': lambda: mp.mpf('6.67430e-11'),
        'formula': "G = F r²/(m₁m₂)",
        'accuracy': "22 ppm",
        'reference': "CODATA 2018"
    },
    "Avogadro’s Number": {
        'func': lambda: mp.mpf('6.02214076e23'),
        'formula': "N_A = Fixed value",
        'accuracy': "Exact",
        'reference': "2019 SI"
    },
    "Permittivity of Free Space": {
        'func': lambda: mp.epsilon0,
        'formula': "ε₀ = 1/(μ₀c²)",
        'accuracy': "Exact definition",
        'reference': "SI units"
    },
    "Permeability of Free Space": {
        'func': lambda: mp.mu0,
        'formula': "μ₀ = 4π × 10⁻⁷ N/A²",
        'accuracy': "Exact definition",
        'reference': "SI units"
    },
    "Wien’s Displacement Constant": {
        'func': lambda: mp.mpf('2.897771955e-3'),
        'formula': "b = hc/(k_B × 4.965114231)",
        'accuracy': "0.013 ppm",
        'reference': "CODATA 2018"
    },
    "Bohr Magneton": {
        'func': lambda: mp.mpf('9.2740100783e-24'),
        'formula': "μ_B = eℏ/(2mₑ)",
        'accuracy': "0.075 ppb",
        'reference': "CODATA 2018"
    },
    "Nuclear Magneton": {
        'func': lambda: mp.mpf('5.0507837461e-27'),
        'formula': "μ_N = eℏ/(2m_p)",
        'accuracy': "0.059 ppb",
        'reference': "CODATA 2018"
    },
    "Hartree Energy": {
        'func': lambda: mp.mpf('4.3597447222071e-18'),
        'formula': "E_h = e²/(4πε₀a₀)",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Quantum of Circulation": {
        'func': lambda: mp.mpf('3.6369475516e-4'),
        'formula': "h/(2mₑ)",
        'accuracy': "0.075 ppb",
        'reference': "CODATA 2018"
    },
    "von Klitzing Constant": {
        'func': lambda: mp.mpf('25812.80745'),
        'formula': "R_K = h/e²",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Josephson Constant": {
        'func': lambda: mp.mpf('483597.8484e9'),
        'formula': "K_J = 2e/h",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Thomson Cross Section": {
        'func': lambda: mp.mpf('6.6524587321e-29'),
        'formula': "σ_e = 8πr_e²/3",
        'accuracy': "0.015 ppm",
        'reference': "CODATA 2018"
    },
    "Classical Electron Radius": {
        'func': lambda: mp.mpf('2.8179403262e-15'),
        'formula': "r_e = e²/(4πε₀mₑc²)",
        'accuracy': "0.015 ppm",
        'reference': "CODATA 2018"
    },
    "Proton Compton Wavelength": {
        'func': lambda: mp.mpf('1.32140985539e-15'),
        'formula': "λ_p = h/(m_pc)",
        'accuracy': "0.059 ppb",
        'reference': "CODATA 2018"
    },
    "Proton Gyromagnetic Ratio": {
        'func': lambda: mp.mpf('2.6752218744e8'),
        'formula': "γ_p = 2μ_p/ℏ",
        'accuracy': "0.023 ppb",
        'reference': "CODATA 2018"
    },
    "Neutron Gyromagnetic Ratio": {
        'func': lambda: mp.mpf('1.83247171e8'),
        'formula': "γ_n = 2μ_n/ℏ",
        'accuracy': "0.33 ppm",
        'reference': "CODATA 2018"
    },
    "Fermi Coupling Constant": {
        'func': lambda: mp.mpf('1.1663787e-5'),
        'formula': "G_F = √2 g²/(8m_W²)",
        'accuracy': "0.6 ppm",
        'reference': "Particle Data Group"
    },
    "Hubble Constant": {
        'func': lambda: mp.mpf('2.25e-18'),
        'formula': "H₀ = v/D",
        'accuracy': "1.8% uncertainty",
        'reference': "Planck 2018"
    },
    "Cosmological Constant": {
        'func': lambda: mp.mpf('1.1056e-52'),
        'formula': "Λ = 8πGρ_vac/c²",
        'accuracy': "Theoretical value",
        'reference': "ΛCDM model"
    },
    "Critical Density of the Universe": {
        'func': lambda: mp.mpf('9.9e-27'),
        'formula': "ρ_c = 3H₀²/(8πG)",
        'accuracy': "1.8% uncertainty",
        'reference': "Friedmann equations"
    },
    "Saha Ionization Constant": {
        'func': lambda: mp.mpf('1.380649e-23'),
        'formula': "K = (2πmₑk_BT)^(3/2)/h³",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Rydberg Unit of Energy": {
        'func': lambda: mp.mpf('13.605693122994'),
        'formula': "Ry = e²/(8πε₀a₀)",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Planck Force": {
        'func': lambda: mp.mpf('1.210256e44'),
        'formula': "F_P = c⁴/G",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Planck Energy": {
        'func': lambda: mp.mpf('1.956081e9'),
        'formula': "E_P = √(ℏc⁵/G)",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Planck Momentum": {
        'func': lambda: mp.mpf('6.52485e24'),
        'formula': "p_P = E_P/c",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Planck Area": {
        'func': lambda: mp.mpf('2.6121e-70'),
        'formula': "A_P = ℓ_P²",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Planck Volume": {
        'func': lambda: mp.mpf('4.2217e-105'),
        'formula': "V_P = ℓ_P³",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Sackur–Tetrode Constant": {
        'func': lambda: mp.mpf('-1.164870523'),
        'formula': "S/k_B = ln(V/N(4πmU/(3h²N))^(3/2)) + 5/2",
        'accuracy': "Theoretical calculation",
        'reference': "Statistical mechanics"
    },
    "Planck Power": {
        'func': lambda: mp.mpf('3.62831e52'),
        'formula': "P_P = E_P/t_P",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Planck Density": {
        'func': lambda: mp.mpf('5.15500e96'),
        'formula': "ρ_P = m_P/ℓ_P³",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Molar Planck Constant": {
        'func': lambda: mp.mpf('3.990312712e-10'),
        'formula': "N_A h",
        'accuracy': "Exact (SI)",
        'reference': "2019 SI"
    },
    "Characteristic Impedance of Free Space": {
        'func': lambda: mp.sqrt(mp.mu0/mp.epsilon0),
        'formula': "Z₀ = √(μ₀/ε₀)",
        'accuracy': "Exact definition",
        'reference': "SI units"
    },
    "Planck Current": {
        'func': lambda: mp.mpf('3.47897e25'),
        'formula': "I_P = q_P/t_P",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Planck Angular Frequency": {
        'func': lambda: mp.mpf('1.85487e43'),
        'formula': "ω_P = 1/t_P",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Planck Acceleration": {
        'func': lambda: mp.mpf('5.56073e51'),
        'formula': "a_P = ℓ_P/t_P²",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Atomic Unit of Time": {
        'func': lambda: mp.mpf('2.4188843265857e-17'),
        'formula': "t₀ = ℏ/E_h",
        'accuracy': "Exact definition",
        'reference': "Atomic units"
    },
    "Planck Frequency": {
        'func': lambda: mp.mpf('1.85487e43'),
        'formula': "ν_P = 1/t_P",
        'accuracy': "0.64 ppm",
        'reference': "Natural units"
    },
    "Atomic Unit of Velocity": {
        'func': lambda: mp.mpf('2187691.26364'),
        'formula': "v₀ = e²/(4πε₀ℏ)",
        'accuracy': "Exact definition",
        'reference': "Atomic units"
    }
}
    # ==================================================================
    # UI Initialization
    # ==================================================================

    def init_ui(self):
        self.setWindowTitle("Ultimate Math Constants Calculator")
        self.setWindowIcon(QIcon("math_icon.png"))
        self.setGeometry(100, 100, 1600, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Left panel
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search 100+ constants...")
        self.search_bar.textChanged.connect(self.filter_list)
        
        # Constants list
        self.constants_list = QListWidget()
        self.constants_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(self.constants_list)

        # Right panel
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_layout = QVBoxLayout(right_panel)

        # Info section
        self.info_label = QLabel("ℹ Select a constant from the list")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Formula display
        self.formula_display = QTextEdit()
        self.formula_display.setReadOnly(True)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        
        # Value display
        self.value_display = QTextEdit()
        self.value_display.setReadOnly(True)
        
        # Control panel
        control_layout = QHBoxLayout()
        self.precision_input = QLineEdit("1000")
        self.precision_input.setPlaceholderText("Precision (e.g., 100, 1K, 1M)")
        self.copy_btn = QPushButton("📋 Copy Value")
        self.save_btn = QPushButton("💾 Save Value")
        
        control_layout.addWidget(QLabel("Precision:"))
        control_layout.addWidget(self.precision_input)
        control_layout.addWidget(self.copy_btn)
        control_layout.addWidget(self.save_btn)

        right_layout.addWidget(self.info_label)
        right_layout.addWidget(self.formula_display)
        right_layout.addWidget(self.progress_bar)
        right_layout.addWidget(self.value_display)
        right_layout.addLayout(control_layout)

        # Add panels to main layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 1000])
        main_layout.addWidget(splitter)

        # Connect signals
        self.constants_list.itemClicked.connect(self.constant_selected)
        self.precision_input.textChanged.connect(self.start_calculation)
        self.copy_btn.clicked.connect(self.copy_value)
        self.save_btn.clicked.connect(self.save_value)

        self.apply_styles()
        self.populate_list()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0d0d0d;
                color: #00ff7f;
            }
            QLineEdit, QTextEdit, QListWidget {
                background-color: #1a1a1a;
                border: 2px solid #00ff7f;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1a1a1a;
                border: 2px solid #00ff7f;
                border-radius: 5px;
                padding: 8px;
                min-width: 100px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #262626;
            }
            QProgressBar {
                border: 2px solid #00ff7f;
                border-radius: 5px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #00ff7f;
            }
            QSplitter::handle {
                background-color: #00ff7f;
                width: 2px;
            }
        """)
        self.formula_display.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #00ff7f;
        """)
        self.value_display.setStyleSheet("""
            font-family: 'Consolas';
            font-size: 14px;
            color: #00ff7f;
        """)
        self.info_label.setStyleSheet("font-size: 16px;")

    # ==================================================================
    # Core Functionality
    # ==================================================================

    def populate_list(self):
        self.constants_list.clear()
        for name in self.constants.keys():
            item = QListWidgetItem(f"✦ {name}")
            item.setData(Qt.ItemDataRole.UserRole, name)
            self.constants_list.addItem(item)

    def filter_list(self):
        search_text = self.search_bar.text().lower()
        for i in range(self.constants_list.count()):
            item = self.constants_list.item(i)
            item.setHidden(search_text not in item.text().lower())

    def constant_selected(self, item):
        self.current_constant = item.data(Qt.ItemDataRole.UserRole)
        self.update_info_display()
        self.start_calculation()

    def update_info_display(self):
        constant_data = self.constants[self.current_constant]
        info_text = f"""
        <b>{self.current_constant}</b><br>
        <i>{constant_data['reference']}</i><br>
        Accuracy: {constant_data['accuracy']}
        """
        self.info_label.setText(info_text)
        self.formula_display.setText(constant_data['formula'])

    def start_calculation(self):
        if self.calculation_thread and self.calculation_thread.isRunning():
            self.calculation_thread.stop()

        precision = self.parse_precision(self.precision_input.text())
        self.progress_bar.setValue(0)
        self.value_display.setPlainText("⌛ Calculating...")

        self.calculation_thread = CalculationThread(
            self.constants[self.current_constant],
            precision
        )
        self.calculation_thread.update_progress.connect(self.update_progress)
        self.calculation_thread.result_ready.connect(self.show_result)
        self.calculation_thread.start()

    def update_progress(self, value, formula):
        self.progress_bar.setValue(value)
        self.formula_display.setText(f"{formula}\n\nProgress: {value}%")

    def show_result(self, result, formula):
        self.progress_bar.setValue(100)
        self.value_display.setPlainText(result)
        self.formula_display.setText(formula)
        self.value_display.moveCursor(QTextCursor.MoveOperation.Start)

    def parse_precision(self, text):
        text = text.strip().upper().replace(" ", "")
        if not text:
            return 100
        multipliers = {'K': 10**3, 'M': 10**6, 'B': 10**9}
        suffix = text[-1] if text[-1] in multipliers else ''
        base = text[:-1] if suffix else text
        
        try:
            num = float(base) * multipliers.get(suffix, 1)
            return min(int(num), 10**6)  # Max 1 million digits
        except:
            return 100

    def copy_value(self):
        QApplication.clipboard().setText(self.value_display.toPlainText())

    def save_value(self):
        options = QFileDialog.Option.ReadOnly
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Constant Value", "", 
            "Text Files (*.txt);;All Files (*)", options=options)
        if filename:
            with open(filename, 'w') as f:
                f.write(f"=== {self.current_constant} ===\n")
                f.write(f"Formula: {self.constants[self.current_constant]['formula']}\n")
                f.write(f"Precision: {self.precision_input.text()}\n\n")
                f.write(self.value_display.toPlainText())

# ======================================================================
# Application Entry Point
# ======================================================================

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ConstantsApp()
    window.show()
    sys.exit(app.exec())

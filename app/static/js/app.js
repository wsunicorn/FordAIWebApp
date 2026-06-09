/**
 * Ford AI WebApp - Premium UI Interactions (Taste-Skill Edition)
 * Implements taste-skill principles: sub-300ms motion, origin-aware transforms,
 * magnetic mouse interactions, parallax, and precise staggered reveals.
 */

// Format currency
const formatVnd = (value) =>
  new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0,
  }).format(Math.max(0, Number(value) || 0));

// Check for reduced motion preference
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const currentLocale = document.documentElement.lang === "en" ? "en" : "vi";
const uiCopy = {
  vi: {
    close: "Đóng",
    success: "Đã nhận yêu cầu. Anh Huy sẽ liên hệ lại sớm.",
    aiError: "Xin lỗi, đang có lỗi kết nối. Vui lòng gọi trực tiếp anh Huy để được hỗ trợ.",
  },
  en: {
    close: "Close",
    success: "Request received. Huy will contact you soon.",
    aiError: "Sorry, there is a connection issue. Please call Huy directly for support.",
  },
};

// Header Scroll Effect
const initHeaderScroll = () => {
  const header = document.getElementById("site-header");
  if (!header) return;

  const onScroll = () => {
    if (window.scrollY > 20) {
      header.classList.add("is-scrolled");
    } else {
      header.classList.remove("is-scrolled");
    }
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll(); // Trigger on load
};

// Mobile Navigation Toggle (Origin-aware popover)
const initMobileNav = () => {
  const navToggle = document.querySelector("[data-nav-toggle]");
  const mobileNav = document.getElementById("mobile-nav");
  
  if (!navToggle || !mobileNav) return;

  navToggle.addEventListener("click", () => {
    const isExpanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isExpanded));
    
    if (!isExpanded) {
      // Open
      mobileNav.style.transformOrigin = "top right";
      mobileNav.classList.add("is-open");
      navToggle.innerHTML = `<span class="material-symbols-outlined">close</span><span data-nav-toggle-label>${uiCopy[currentLocale].close}</span>`;
    } else {
      // Close
      mobileNav.classList.remove("is-open");
      navToggle.innerHTML = '<span class="material-symbols-outlined">menu</span><span data-nav-toggle-label>Menu</span>';
    }
  });

  document.addEventListener("click", (e) => {
    if (mobileNav.classList.contains("is-open") && !navToggle.contains(e.target) && !mobileNav.contains(e.target)) {
      mobileNav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.innerHTML = '<span class="material-symbols-outlined">menu</span><span data-nav-toggle-label>Menu</span>';
    }
  });
};

// Scroll Reveal with Staggered Groups
const initScrollReveal = () => {
  const revealElements = document.querySelectorAll(
    ".bento-grid > *, .process-step, .glass-panel, .section-title, .calc-panel, .card, .promo-grid > *"
  );
  
  if (!revealElements.length) return;

  if (prefersReducedMotion) {
    revealElements.forEach(el => el.classList.add("is-visible"));
    return;
  }

  // Setup elements initially
  revealElements.forEach(el => {
    el.classList.add("reveal-on-scroll");
  });

  // Track currently intersecting items for staggering
  let intersectingQueue = [];
  let isProcessingQueue = false;

  const processQueue = () => {
    if (!intersectingQueue.length) {
      isProcessingQueue = false;
      return;
    }
    
    // Sort by vertical position to ensure top-down stagger
    intersectingQueue.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
    
    intersectingQueue.forEach((el, index) => {
      // 75ms stagger gap between items in the same viewport frame
      setTimeout(() => {
        el.classList.add("is-visible");
      }, index * 75);
    });
    
    intersectingQueue = [];
    isProcessingQueue = false;
  };

  const observer = new IntersectionObserver((entries, observer) => {
    let newIntersections = false;
    
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        intersectingQueue.push(entry.target);
        observer.unobserve(entry.target);
        newIntersections = true;
      }
    });

    if (newIntersections && !isProcessingQueue) {
      isProcessingQueue = true;
      requestAnimationFrame(processQueue);
    }
  }, {
    rootMargin: "0px 0px -50px 0px",
    threshold: 0.1
  });

  revealElements.forEach(el => observer.observe(el));
};

const initConfirmActions = () => {
  const forms = document.querySelectorAll("form[data-confirm]");
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      const message = form.getAttribute("data-confirm");
      if (message && !window.confirm(message)) {
        event.preventDefault();
      }
    });
  });
};

const initLanguagePersistence = () => {
  if (currentLocale === "vi") return;

  document.querySelectorAll('a[href^="/"]').forEach((link) => {
    const rawHref = link.getAttribute("href");
    if (!rawHref || rawHref.startsWith("/api") || rawHref.includes("lang=")) return;
    const url = new URL(rawHref, window.location.origin);
    url.searchParams.set("lang", currentLocale);
    link.setAttribute("href", `${url.pathname}${url.search}${url.hash}`);
  });

  document.querySelectorAll('input[name="redirect_to"]').forEach((input) => {
    if (!(input instanceof HTMLInputElement)) return;
    const url = new URL(input.value || window.location.pathname, window.location.origin);
    url.searchParams.set("lang", currentLocale);
    input.value = `${url.pathname}${url.search}${url.hash}`;
  });
};

// Parallax Effect for Backgrounds
const initParallax = () => {
  if (prefersReducedMotion) return;
  
  const layers = document.querySelectorAll("[data-parallax]");
  if (!layers.length) return;

  let lastScrollY = window.scrollY;
  let ticking = false;

  const updateParallax = () => {
    layers.forEach(layer => {
      const speed = parseFloat(layer.getAttribute("data-parallax") || "0.2");
      const rect = layer.parentElement.getBoundingClientRect();
      
      // Only animate if in viewport
      if (rect.top <= window.innerHeight && rect.bottom >= 0) {
        // Calculate offset based on scroll position relative to element
        const yPos = (rect.top * speed) * -1;
        layer.style.transform = `translateY(${yPos}px)`;
      }
    });
    ticking = false;
  };

  window.addEventListener("scroll", () => {
    lastScrollY = window.scrollY;
    if (!ticking) {
      requestAnimationFrame(updateParallax);
      ticking = true;
    }
  }, { passive: true });
};
// Vehicle Search Filter with Smooth Height/Opacity transition
const initVehicleSearch = () => {
  const searchInput = document.querySelector("[data-vehicle-search]");
  const vehicleCards = document.querySelectorAll("[data-vehicle-card]");
  const emptyState = document.querySelector("[data-empty-vehicles]");

  if (!searchInput || !vehicleCards.length) return;

  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase().trim();
    let hasVisible = false;

    vehicleCards.forEach(card => {
      const name = (card.dataset.name || "").toLowerCase();
      const category = (card.dataset.category || "").toLowerCase();
      
      const isVisible = name.includes(term) || category.includes(term);
      
      if (isVisible) {
        if (card.style.display === "none" || !card.style.display) {
          card.style.display = "";
          // Micro-animation for returning cards
          requestAnimationFrame(() => {
            card.style.opacity = "0";
            card.style.transform = "scale(0.96)";
            requestAnimationFrame(() => {
              card.style.transition = "opacity 200ms ease-out, transform 200ms ease-out";
              card.style.opacity = "1";
              card.style.transform = "scale(1)";
            });
          });
        }
        hasVisible = true;
      } else {
        card.style.display = "none";
      }
    });

    if (emptyState) {
      emptyState.style.display = hasVisible ? "none" : "block";
    }
  });
};

// Success Notice (from URL param)
const initSuccessNotice = () => {
  const params = new URLSearchParams(window.location.search);
  if (params.get("lead") === "success") {
    params.delete("lead");
    const query = params.toString();
    window.history.replaceState({}, document.title, `${window.location.pathname}${query ? `?${query}` : ""}`);
    
    requestAnimationFrame(() => {
      const form = document.querySelector("form");
      if (form) {
        const notice = document.createElement("div");
        notice.className = "mb-6 rounded-xl border border-success bg-success/10 px-4 py-3 text-sm font-semibold text-success flex items-center gap-2";
        // Animate in
        notice.style.opacity = "0";
        notice.style.transform = "translateY(-10px)";
        notice.style.transition = "opacity 300ms cubic-bezier(0.23, 1, 0.32, 1), transform 300ms cubic-bezier(0.23, 1, 0.32, 1)";
        
        notice.innerHTML = `<span class="material-symbols-outlined">check_circle</span> ${uiCopy[currentLocale].success}`;
        form.prepend(notice);
        
        requestAnimationFrame(() => {
          notice.style.opacity = "1";
          notice.style.transform = "translateY(0)";
        });
      }
    });
  }
};

// Smooth Number Counter (for calculators)
const animateNumber = (element, targetValue, duration = 400) => {
  if (prefersReducedMotion) {
    element.textContent = formatVnd(targetValue);
    return;
  }
  
  const startValue = parseInt(element.dataset.currentValue || "0", 10);
  const startTime = performance.now();
  
  const updateNumber = (currentTime) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // easeOutQuad
    const easeProgress = progress * (2 - progress);
    const currentValue = Math.floor(startValue + (targetValue - startValue) * easeProgress);
    
    element.textContent = formatVnd(currentValue);
    
    if (progress < 1) {
      requestAnimationFrame(updateNumber);
    } else {
      element.dataset.currentValue = targetValue;
    }
  };
  
  requestAnimationFrame(updateNumber);
};

// Calculators Logic
const initCalculators = () => {
  // On-Road Calculator
  const onRoadForm = document.querySelector("[data-on-road-calculator]");
  if (onRoadForm) {
    const priceInput = onRoadForm.querySelector("[data-calc-price]");
    const insuranceInput = onRoadForm.querySelector("[data-physical-insurance]");
    const totalEl = onRoadForm.querySelector("[data-on-road-total]");
    const regFeeEl = onRoadForm.querySelector("[data-registration-fee]");
    
    const calculateOnRoad = () => {
      const price = Number(priceInput?.value || 0);
      const insurance = Number(insuranceInput?.value || 0);
      const regFee = Math.round(price * 0.072); // Estimate
      const fixedFees = 340000 + 1560000 + 480000;
      const total = price + regFee + fixedFees + insurance;
      
      if (regFeeEl) regFeeEl.textContent = formatVnd(regFee);
      if (totalEl) animateNumber(totalEl, total);
    };
    
    onRoadForm.addEventListener("change", calculateOnRoad);
    onRoadForm.addEventListener("input", calculateOnRoad);
    calculateOnRoad();
  }

  // Loan Calculator
  const loanForm = document.querySelector("[data-loan-calculator]");
  if (loanForm) {
    const priceInput = loanForm.querySelector("[data-loan-price]");
    const downPaymentRange = loanForm.querySelector("[data-down-payment-range]");
    const termInput = loanForm.querySelector("[data-loan-term]");
    const monthlyEl = loanForm.querySelector("[data-monthly-payment]");
    const downValueEl = loanForm.querySelector("[data-down-payment-value]");
    
    const calculateLoan = () => {
      const price = Number(priceInput?.value || 0);
      const downPercent = Number(downPaymentRange?.value || 20) / 100;
      const term = Number(termInput?.value || 84);
      const annualRate = 0.085; // 8.5% default rate
      
      const downPayment = Math.round(price * downPercent);
      const principal = Math.max(0, price - downPayment);
      const monthlyRate = annualRate / 12;
      
      const monthly = monthlyRate > 0 
        ? (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -term))
        : principal / term;
        
      if (downValueEl) downValueEl.textContent = formatVnd(downPayment);
      if (monthlyEl) animateNumber(monthlyEl, Math.round(monthly));
    };
    
    loanForm.addEventListener("change", calculateLoan);
    loanForm.addEventListener("input", calculateLoan);
    calculateLoan();
  }
};

// AI Chat Handlers
const initAiChat = () => {
  const aiChat = document.querySelector("[data-ai-chat]");
  if (!aiChat) return;

  const messagesArea = aiChat.querySelector("[data-ai-messages]");
  const form = aiChat.querySelector("[data-ai-form]");
  const input = form?.querySelector("textarea");
  const submitBtn = form?.querySelector("button[type='submit']");
  
  const getSessionId = () => {
    let id = localStorage.getItem("ford_ai_session_id");
    if (!id) {
      id = "session-" + Math.random().toString(36).substring(2, 15);
      localStorage.setItem("ford_ai_session_id", id);
    }
    return id;
  };

  const appendMessage = (content, isUser = false) => {
    const div = document.createElement("div");
    div.className = `message-bubble ${isUser ? 'message-user' : 'message-assistant'}`;
    div.textContent = content;
    messagesArea.appendChild(div);
    
    messagesArea.scrollTo({
      top: messagesArea.scrollHeight,
      behavior: prefersReducedMotion ? 'auto' : 'smooth'
    });
  };

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    
    appendMessage(text, true);
    input.value = "";
    input.style.height = "auto";
    
    if (submitBtn) submitBtn.disabled = true;
    
    const typingId = "typing-" + Date.now();
    const typingDiv = document.createElement("div");
    typingDiv.id = typingId;
    typingDiv.className = "message-bubble message-assistant opacity-70";
    typingDiv.innerHTML = '<span class="material-symbols-outlined animate-pulse">more_horiz</span>';
    messagesArea.appendChild(typingDiv);
    messagesArea.scrollTo({ top: messagesArea.scrollHeight, behavior: 'smooth' });

    try {
      const res = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, session_id: getSessionId() })
      });
      
      const data = await res.json();
      document.getElementById(typingId)?.remove();
      appendMessage(data.answer, false);
      
    } catch (err) {
      document.getElementById(typingId)?.remove();
      appendMessage(uiCopy[currentLocale].aiError, false);
    } finally {
      if (submitBtn) submitBtn.disabled = false;
      input.focus();
    }
  });

  input?.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 120) + "px";
  });
  
  input?.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit"));
    }
  });
};

// Initialize everything on DOM Content Loaded
document.addEventListener("DOMContentLoaded", () => {
  initHeaderScroll();
  initMobileNav();
  initConfirmActions();
  initLanguagePersistence();
  initScrollReveal();
  initParallax();
  initVehicleSearch();
  initSuccessNotice();
  initCalculators();
  initAiChat();
});

/**
 * PATHWAY AI - Hero Section Interactive Animation Engine
 * 1. Particle Neural Pathway Canvas (Mouse-reactive, 60fps, energy pulses)
 * 2. Live Pathway AI Simulator (Auto-cycling & interactive student persona mapper)
 */

(function () {
  // Wait for DOM
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHeroAnimations);
  } else {
    initHeroAnimations();
  }

  function initHeroAnimations() {
    initNeuralCanvas();
    initPersonaSimulator();
  }

  /* -------------------------------------------------------------
   * 1. NEURAL CAREER PATHWAY CANVAS
   * ----------------------------------------------------------- */
  function initNeuralCanvas() {
    const canvas = document.getElementById("heroPathwayCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let width, height;
    let animationFrameId = null;
    let isVisible = true;

    // Node definitions (Career vertices and Indian Education milestones)
    const labels = [
      "Class 10th", "Class 12th", "JEE Adv", "NEET UG", "CUET", "UPSC", 
      "CA Foundation", "AI Engineer", "Doctor (MBBS)", "Chartered Accountant", 
      "Data Scientist", "IAS Officer", "Cybersecurity", "Architect", "Biotech"
    ];

    let nodes = [];
    let pulses = [];
    let mouse = { x: -1000, y: -1000, active: false };

    function resize() {
      const rect = canvas.parentElement.getBoundingClientRect();
      width = canvas.width = rect.width * (window.devicePixelRatio || 1);
      height = canvas.height = rect.height * (window.devicePixelRatio || 1);
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
      ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
      createNodes(rect.width, rect.height);
    }

    function createNodes(w, h) {
      nodes = [];
      const count = Math.min(Math.floor(w / 45), 26);
      for (let i = 0; i < count; i++) {
        const label = labels[i % labels.length];
        nodes.push({
          x: Math.random() * (w - 60) + 30,
          y: Math.random() * (h - 60) + 30,
          vx: (Math.random() - 0.5) * 0.45,
          vy: (Math.random() - 0.5) * 0.45,
          radius: i < labels.length ? 4.5 : 2.5,
          label: i < 14 ? label : null,
          color: (i % 3 === 0) ? "#0071E3" : (i % 3 === 1) ? "#8057E8" : "#00C853",
          pulseTimer: Math.random() * 100
        });
      }
    }

    // Passive mouse move listener
    canvas.parentElement.addEventListener("mousemove", (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
      mouse.active = true;
    }, { passive: true });

    canvas.parentElement.addEventListener("mouseleave", () => {
      mouse.active = false;
    });

    // Spawn pulses along connection lines
    function spawnPulses() {
      if (pulses.length > 10) return;
      if (nodes.length < 2) return;
      const n1 = nodes[Math.floor(Math.random() * nodes.length)];
      // Find nearest neighbor
      let bestDist = Infinity;
      let n2 = null;
      for (let other of nodes) {
        if (other === n1) continue;
        const dx = other.x - n1.x;
        const dy = other.y - n1.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 180 && dist < bestDist) {
          bestDist = dist;
          n2 = other;
        }
      }
      if (n2) {
        pulses.push({
          x: n1.x,
          y: n1.y,
          targetX: n2.x,
          targetY: n2.y,
          progress: 0,
          speed: 0.015 + Math.random() * 0.02,
          color: n1.color
        });
      }
    }

    function draw() {
      if (!isVisible) return;

      const rect = canvas.parentElement.getBoundingClientRect();
      const w = rect.width;
      const h = rect.height;

      ctx.clearRect(0, 0, w, h);

      // Update and connect nodes
      for (let i = 0; i < nodes.length; i++) {
        const n1 = nodes[i];
        n1.x += n1.vx;
        n1.y += n1.vy;

        // Bounce from bounds
        if (n1.x < 20 || n1.x > w - 20) n1.vx *= -1;
        if (n1.y < 20 || n1.y > h - 20) n1.vy *= -1;

        // Draw connections
        for (let j = i + 1; j < nodes.length; j++) {
          const n2 = nodes[j];
          const dx = n2.x - n1.x;
          const dy = n2.y - n1.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 150) {
            const alpha = (1 - dist / 150) * 0.28;
            ctx.beginPath();
            ctx.moveTo(n1.x, n1.y);
            ctx.lineTo(n2.x, n2.y);
            ctx.strokeStyle = `rgba(0, 113, 227, ${alpha})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }

        // Mouse interaction beam
        if (mouse.active) {
          const mdx = mouse.x - n1.x;
          const mdy = mouse.y - n1.y;
          const mdist = Math.sqrt(mdx * mdx + mdy * mdy);
          if (mdist < 140) {
            const malpha = (1 - mdist / 140) * 0.55;
            ctx.beginPath();
            ctx.moveTo(n1.x, n1.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.strokeStyle = `rgba(128, 87, 232, ${malpha})`;
            ctx.lineWidth = 1.4;
            ctx.stroke();
          }
        }

        // Draw node circle with soft glow
        ctx.beginPath();
        ctx.arc(n1.x, n1.y, n1.radius, 0, Math.PI * 2);
        ctx.fillStyle = n1.color;
        ctx.shadowColor = n1.color;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.shadowBlur = 0; // reset

        // Draw node label if present
        if (n1.label && w > 640) {
          ctx.font = "500 10.5px -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif";
          ctx.fillStyle = "rgba(16, 42, 86, 0.65)";
          ctx.fillText(n1.label, n1.x + 8, n1.y + 3);
        }
      }

      // Update & draw pulses (energy packets traveling between milestones)
      if (Math.random() < 0.08) spawnPulses();

      for (let pIdx = pulses.length - 1; pIdx >= 0; pIdx--) {
        const p = pulses[pIdx];
        p.progress += p.speed;
        if (p.progress >= 1) {
          pulses.splice(pIdx, 1);
          continue;
        }
        const curX = p.x + (p.targetX - p.x) * p.progress;
        const curY = p.y + (p.targetY - p.y) * p.progress;

        ctx.beginPath();
        ctx.arc(curX, curY, 3, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 10;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      animationFrameId = requestAnimationFrame(draw);
    }

    // Optimization: Pause when hero is scrolled out of viewport
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        isVisible = entry.isIntersecting;
        if (isVisible && !animationFrameId) {
          animationFrameId = requestAnimationFrame(draw);
        } else if (!isVisible && animationFrameId) {
          cancelAnimationFrame(animationFrameId);
          animationFrameId = null;
        }
      });
    }, { threshold: 0.1 });

    observer.observe(canvas.parentElement);

    window.addEventListener("resize", () => {
      resize();
    });

    resize();
    animationFrameId = requestAnimationFrame(draw);
  }

  /* -------------------------------------------------------------
   * 2. LIVE PATHWAY AI SIMULATOR
   * ----------------------------------------------------------- */
  function initPersonaSimulator() {
    const container = document.getElementById("heroSimulator");
    if (!container) return;

    const personas = [
      {
        id: "school",
        title: "8th–10th School Aspirant",
        badge: "Foundation Stage",
        skills: [
          { name: "Logical & Spatial Reasoning", val: 92 },
          { name: "Mathematical Foundations", val: 89 },
          { name: "Scientific Curiosity", val: 95 }
        ],
        pathway: [
          { step: "Class 10th", desc: "CBSE / ICSE Board" },
          { step: "Stream Pick", desc: "Science (PCM / AI)" },
          { step: "Target Exam", desc: "JEE Main & Advanced" },
          { step: "Career Goal", desc: "Artificial Intelligence Eng." }
        ],
        career: "Artificial Intelligence Engineer",
        category: "Science & Technology",
        match: 96.4,
        salary: "₹14 - 38 LPA",
        exam: "JEE Advanced / B.Tech AI",
        icon: "🤖"
      },
      {
        id: "pcb",
        title: "11th–12th PCB Student",
        badge: "Medical Stream",
        skills: [
          { name: "Biological Comprehension", val: 96 },
          { name: "Verbal & Abstract Ability", val: 91 },
          { name: "Empathy & Clinical Focus", val: 94 }
        ],
        pathway: [
          { step: "Class 12th", desc: "PCB 50%+ Marks" },
          { step: "Entrance", desc: "NEET UG Qualified" },
          { step: "College", desc: "AIIMS / Top Govt GMC" },
          { step: "Career Goal", desc: "Doctor (MBBS) & MD" }
        ],
        career: "Doctor (MBBS)",
        category: "Science & Healthcare",
        match: 98.1,
        salary: "₹10 - 32 LPA",
        exam: "NEET UG (NTA)",
        icon: "🩺"
      },
      {
        id: "commerce",
        title: "11th–12th Commerce Student",
        badge: "Finance & Corporate",
        skills: [
          { name: "Numerical & Financial Analysis", val: 95 },
          { name: "Audit & Regulatory Acumen", val: 93 },
          { name: "Critical Problem Solving", val: 90 }
        ],
        pathway: [
          { step: "Class 12th", desc: "Commerce / Math" },
          { step: "Foundation", desc: "ICAI CA Foundation" },
          { step: "Articleship", desc: "3-Yr Practical Training" },
          { step: "Career Goal", desc: "Chartered Accountant (CA)" }
        ],
        career: "Chartered Accountant (CA)",
        category: "Commerce & Business",
        match: 95.8,
        salary: "₹12 - 30 LPA",
        exam: "ICAI Examination",
        icon: "📊"
      },
      {
        id: "grad",
        title: "College / Graduation Student",
        badge: "Civil Services & Leadership",
        skills: [
          { name: "Public Policy & Analytical Thinking", val: 94 },
          { name: "Verbal & Essay Articulation", val: 93 },
          { name: "Decision Making Under Pressure", val: 96 }
        ],
        pathway: [
          { step: "Bachelor's", desc: "Any UGC Recognized Degree" },
          { step: "Prelims", desc: "UPSC CSE GS + CSAT" },
          { step: "Mains & Interview", desc: "Personality Test at Dholpur" },
          { step: "Career Goal", desc: "IAS Officer (Indian Admin)" }
        ],
        career: "IAS Officer",
        category: "Governance & Humanities",
        match: 97.2,
        salary: "₹10 - 28 LPA (Govt Perks)",
        exam: "UPSC Civil Services",
        icon: "🏛️"
      }
    ];

    let currentIndex = 0;
    let autoCycleTimer = null;

    // Render interactive chips
    const chipsContainer = document.getElementById("simChips");
    if (chipsContainer) {
      chipsContainer.innerHTML = personas.map((p, idx) => `
        <button type="button" class="sim-chip ${idx === 0 ? 'active' : ''}" data-index="${idx}">
          ${p.title}
        </button>
      `).join("");

      chipsContainer.querySelectorAll(".sim-chip").forEach(chip => {
        chip.addEventListener("click", (e) => {
          const idx = parseInt(chip.getAttribute("data-index"), 10);
          switchPersona(idx);
          resetTimer();
        });
      });
    }

    function switchPersona(index) {
      currentIndex = index;
      const p = personas[index];

      // Update chip active states
      if (chipsContainer) {
        chipsContainer.querySelectorAll(".sim-chip").forEach((c, idx) => {
          c.classList.toggle("active", idx === index);
        });
      }

      // Update persona badge and details
      const badgeElem = document.getElementById("simPersonaBadge");
      if (badgeElem) badgeElem.textContent = p.badge;

      // Update Skill bars with smooth animated fill
      const skillsContainer = document.getElementById("simSkills");
      if (skillsContainer) {
        skillsContainer.innerHTML = p.skills.map(s => `
          <div class="sim-skill-row">
            <div class="sim-skill-label">
              <span>${s.name}</span>
              <span class="sim-skill-val">${s.val}%</span>
            </div>
            <div class="sim-skill-track">
              <div class="sim-skill-bar" style="width: 0%;" data-target="${s.val}%"></div>
            </div>
          </div>
        `).join("");

        // Trigger width animation on next tick
        setTimeout(() => {
          skillsContainer.querySelectorAll(".sim-skill-bar").forEach(bar => {
            bar.style.width = bar.getAttribute("data-target");
          });
        }, 30);
      }

      // Update 4-step dynamic pathway with pulse sequence
      const pathContainer = document.getElementById("simPathwaySteps");
      if (pathContainer) {
        pathContainer.innerHTML = p.pathway.map((step, idx) => `
          <div class="sim-path-node ${idx === 3 ? 'final' : ''}">
            <div class="sim-node-circle">
              <span>${idx + 1}</span>
            </div>
            <div class="sim-node-info">
              <div class="sim-node-step">${step.step}</div>
              <div class="sim-node-desc">${step.desc}</div>
            </div>
          </div>
        `).join("");
      }

      // Update top match card
      const iconElem = document.getElementById("simCareerIcon");
      if (iconElem) iconElem.textContent = p.icon;

      const titleElem = document.getElementById("simCareerTitle");
      if (titleElem) titleElem.textContent = p.career;

      const catElem = document.getElementById("simCareerCategory");
      if (catElem) catElem.textContent = p.category;

      const salaryElem = document.getElementById("simCareerSalary");
      if (salaryElem) salaryElem.textContent = p.salary;

      const examElem = document.getElementById("simCareerExam");
      if (examElem) examElem.textContent = p.exam;

      // Animate circular match meter
      const matchScoreElem = document.getElementById("simMatchScore");
      const matchCircle = document.getElementById("simMatchCircle");
      if (matchScoreElem && matchCircle) {
        matchScoreElem.textContent = `${p.match}%`;
        const offset = 220 - (220 * (p.match / 100));
        matchCircle.style.strokeDashoffset = offset;
      }
    }

    function resetTimer() {
      if (autoCycleTimer) clearInterval(autoCycleTimer);
      autoCycleTimer = setInterval(() => {
        currentIndex = (currentIndex + 1) % personas.length;
        switchPersona(currentIndex);
      }, 5000);
    }

    // Initialize first persona
    switchPersona(0);
    resetTimer();

    // Pause cycling on hover
    container.addEventListener("mouseenter", () => {
      if (autoCycleTimer) clearInterval(autoCycleTimer);
    });
    container.addEventListener("mouseleave", () => {
      resetTimer();
    });
  }
})();

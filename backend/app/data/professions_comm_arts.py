# -*- coding: utf-8 -*-

def get_comm_arts_questions():
    questions = []

    careers_data = [
        ("chartered-accountant-ca", "Chartered Accountant (CA)", "accounting_audit_tax", [
            ("What does the 'Accrual Concept' mandate in Indian Accounting Standards (Ind AS)?", "Revenues and expenses are recognized when earned or incurred, regardless of when cash is physically received or paid", "Accrual Accounting Principles"),
            ("Under the Indian Goods and Services Tax (GST) framework, what is Input Tax Credit (ITC)?", "Credit received for GST paid on business inputs/purchases that can offset output tax liability on sales", "Indian GST Compliance (CBIC)"),
            ("What is the primary role of Standards on Auditing (SA) issued by ICAI?", "Prescribe mandatory professional conduct, evidence gathering, and reporting standards for statutory auditors", "ICAI Auditing Standards"),
            ("What does the Current Ratio (Current Assets / Current Liabilities) measure in financial statement analysis?", "Short-term liquidity and capacity of a firm to settle debt obligations due within one operating year", "Liquidity Ratio Analysis"),
            ("Under the Indian Income Tax Act 1961, what is Tax Deducted at Source (TDS)?", "Indirect collection mechanism where tax is deducted at the point of origin of income by the payer", "Income Tax Statutory Withholding"),
            ("What constitutes 'Materiality' in corporate auditing?", "Information whose omission or misstatement could reasonably influence the economic decisions of financial statement users", "Audit Materiality Thresholds"),
            ("What is the difference between Capital Expenditure and Revenue Expenditure?", "Capital expenditure yields enduring economic benefits over multiple financial years; revenue expenditure funds current operations", "Capital vs Revenue Accounting"),
            ("What does a qualified audit report opinion issued by a statutory auditor signify?", "Financial statements are fairly presented EXCEPT for a specific, isolated material issue that does not pervade the entire accounts", "Audit Opinions & Qualifications"),
            ("In cost accounting, what is the Break-Even Point?", "Sales volume where total revenues exactly equal total costs (fixed + variable), generating zero profit or loss", "Marginal Costing & Break-Even"),
            ("What is the statutory requirement under Companies Act 2013 regarding Corporate Social Responsibility (CSR)?", "Eligible companies must spend minimum 2% of average net profits of preceding 3 years on approved CSR activities", "Companies Act CSR Provisions")
        ]),
        ("investment-banker", "Investment Banker", "investment_banking_mna", [
            ("What does an Initial Public Offering (IPO) enable a private corporation to achieve?", "Raise capital from public institutional and retail investors and list equity shares on stock exchanges", "Equity Capital Markets (ECM)"),
            ("In Discounted Cash Flow (DCF) modeling, what discount rate is used to discount Free Cash Flows to Firm (FCFF)?", "Weighted Average Cost of Capital (WACC)", "DCF Valuation & WACC"),
            ("What does a Leveraged Buyout (LBO) transaction involve?", "Acquisition of a company primarily funded with significant debt borrowed against the target firm's assets and cash flows", "LBO Deal Structuring"),
            ("What is 'Due Diligence' in Mergers and Acquisitions (M&A)?", "Comprehensive financial, legal, operational, and tax audit of the target company before closing a deal", "M&A Due Diligence"),
            ("What is the difference between Enterprise Value (EV) and Equity Value (Market Cap)?", "Enterprise Value = Equity Value + Total Debt - Cash & Cash Equivalents (reflecting total business operating value)", "Enterprise Valuation Multiples"),
            ("In debt capital markets, what is a 'Debt Covenant' in loan agreements?", "Binding contractual restriction placed on a borrower to maintain credit metrics (e.g. Max Debt/EBITDA ratio)", "Debt Covenants & Syndicate Loans"),
            ("What does the 'Pitchbook' represent in investment banking client advisory?", "A persuasive strategic presentation outlining market trends, target valuation, and proposed M&A transaction rationales", "Client Pitch & Valuation Memos"),
            ("What does 'Accretive Acquisition' mean in corporate M&A deals?", "A merger that increases the acquiring company's post-deal Earnings Per Share (EPS)", "Accretion/Dilution Analysis"),
            ("What is the role of an Underwriter in an equity capital offering?", "Financial institution that assumes risk of buying securities from issuer and reselling them to investors (book building)", "Book Building & Underwriting"),
            ("What is Private Equity Growth Capital?", "Investment of institutional equity capital into mature, unlisted private businesses to finance expansion or buyout", "Private Equity Structures")
        ]),
        ("financial-analyst", "Financial Analyst", "financial_analysis", [
            ("What does the Capital Asset Pricing Model (CAPM) calculate?", "Expected return on an asset based on risk-free rate, its market beta (systematic risk), and market risk premium", "CAPM & Cost of Equity"),
            ("What does a stock's Beta measure in financial markets?", "The volatility or systematic risk of a stock relative to the overall market portfolio", "Beta & Systematic Risk"),
            ("What is Net Present Value (NPV) in capital budgeting decisions?", "Present value of future cash inflows minus initial capital cash outlay; accept project if NPV > 0", "Capital Budgeting NPV"),
            ("What does the DuPont Analysis formula decompose Return on Equity (ROE) into?", "Net Profit Margin x Asset Turnover x Financial Leverage Multiplier", "DuPont ROE Decomposition"),
            ("In bond valuation, what is the inverse relationship between Bond Prices and Yield to Maturity (YTM)?", "When market interest rates (yields) rise, existing bond market prices fall", "Fixed Income Bond Duration"),
            ("What is Free Cash Flow to Equity (FCFE)?", "Cash flow available to equity shareholders after operating expenses, taxes, debt payments, and reinvestment needs", "Equity Cash Flow Modeling"),
            ("What does the Debt-to-Equity (D/E) ratio indicate to credit rating analysts?", "The proportion of company financing sourced from debt creditors compared to shareholder equity", "Capital Structure & Solvency"),
            ("What is 'Quantitative Easing' practiced by global central banks?", "Monetary policy where central bank buys government bonds to inject direct liquidity into the commercial banking system", "Macroeconomics & Liquidity"),
            ("What does an inverted Yield Curve historically signal in macroeconomic forecasting?", "Higher short-term interest rates than long-term rates, historically preceding an economic recession", "Yield Curve Macro Forecasting"),
            ("What is Sensitivity Analysis in financial spreadsheet modeling?", "Testing how changes in key underlying assumptions (e.g. sales growth, interest rates) impact financial outputs", "Financial Scenario Modeling")
        ]),
        ("business-manager", "Business Manager", "business_operations_mgmt", [
            ("What is the primary purpose of a Balanced Scorecard in corporate performance management?", "Track strategic performance across Financial, Customer, Internal Process, and Learning & Growth perspectives", "Balanced Scorecard Framework"),
            ("In operations management, what is the Theory of Constraints (TOC)?", "Focus on identifying the single most critical bottleneck constraining overall operational throughput and optimizing it", "Operations Theory of Constraints"),
            ("What is the difference between Transformational Leadership and Transactional Leadership?", "Transformational inspires followers to innovate and exceed targets; transactional relies on formal rewards and contingent compliance", "Leadership Theory & Styles"),
            ("In strategic management, what does Porter's Five Forces framework evaluate?", "Industry attractiveness and competitive intensity (Rivalry, Entrants, Substitutes, Buyer Power, Supplier Power)", "Porter's Industry Analysis"),
            ("What is the primary role of Key Performance Indicators (KPIs) in team management?", "Quantifiable metrics that measure organizational success in achieving key strategic business objectives", "KPI Architecture & Governance"),
            ("In conflict resolution, what is the 'Collaborating' style on the Thomas-Kilmann Conflict Mode Instrument?", "High assertiveness and high cooperativeness: working together to find a win-win solution addressing all core concerns", "Executive Conflict Resolution"),
            ("What does 'SWOT Analysis' structure for an enterprise strategic planning session?", "Internal Strengths & Weaknesses; External Opportunities & Threats", "SWOT Strategic Planning"),
            ("What is Change Management (e.g. Kotter's 8-Step Model) designed to accomplish in corporate restructuring?", "Guide organizational transitions smoothly by creating urgency, building coalitions, and institutionalizing new culture", "Organizational Change Management"),
            ("In human resource management, what is 360-degree performance appraisal?", "Gathering feedback on an employee from supervisors, peers, subordinates, and self-evaluation", "Multisource Performance Review"),
            ("What does 'Lean Management' eliminate across business processes?", "Muda (wasteful activities that consume resources without adding value for the customer)", "Lean Process Optimization")
        ]),
        ("entrepreneur", "Entrepreneur", "entrepreneurship_venture", [
            ("What is 'Product-Market Fit' (PMF) in venture building?", "The point where a startup's product satisfies strong market demand and customers spontaneously recommend it", "Product-Market Fit Verification"),
            ("What is 'Unit Economics' in startup financial sustainability?", "Direct revenues and costs associated with a single unit of business (e.g. Customer Lifetime Value vs Acquisition Cost)", "LTV/CAC Unit Economics"),
            ("What does 'Bootstrapping' mean in entrepreneurial financing?", "Building a business using founder personal savings and early customer cash flow without outside institutional venture capital", "Venture Bootstrapping"),
            ("What is a 'Pivot' in the Lean Startup methodology?", "Structured course correction in strategy designed to test a new fundamental hypothesis about product or business model", "Strategic Venture Pivoting"),
            ("What is Customer Acquisition Cost (CAC)?", "Total sales and marketing expenditure divided by the total number of new customers acquired during that period", "Customer Acquisition Economics"),
            ("What does a Term Sheet represent when raising Venture Capital (VC) funding?", "Non-binding agreement outlining basic investment terms, company pre-money valuation, governance rights, and liquidation preferences", "Venture Capital Term Sheets"),
            ("What is 'Churn Rate' in subscription-based business models?", "The percentage of subscribers or customers who cancel or do not renew their service over a given time interval", "SaaS Retention & Churn Metrics"),
            ("In intellectual property management, what protection does a Patent provide to an inventor?", "Exclusive legal right granted by government to prevent others from commercially making, using, or selling the invention for 20 years", "Patent Strategy & IP Rights"),
            ("What is 'Design Thinking' empathy mapping in early customer discovery?", "Synthesizing what target customers Say, Think, Do, and Feel to uncover unarticulated emotional and functional pain points", "Customer Discovery Interviews"),
            ("What is a 'Network Effect' competitive moat in platform businesses?", "When a product or service becomes exponentially more valuable to every user as additional users join the network", "Platform Network Effects")
        ]),
        ("marketing-manager", "Marketing Manager", "marketing_brand_strategy", [
            ("What are the traditional '4 Ps' of the Marketing Mix?", "Product, Price, Place, and Promotion", "Marketing Mix Foundations"),
            ("What is 'Brand Positioning' in strategic marketing?", "The distinct mental space and value perception a brand occupies in target consumer minds relative to competitors", "Brand Strategy Positioning"),
            ("In digital marketing analytics, what is Click-Through Rate (CTR)?", "Percentage of people who click on a digital advertisement or link after viewing it (Clicks / Impressions)", "Digital Performance Analytics"),
            ("What does 'Search Engine Optimization' (SEO) achieve for website visibility?", "Optimizing content, keywords, and technical structure to earn high organic (non-paid) search engine ranking positions", "Organic SEO Architecture"),
            ("What is 'Conversion Rate' in e-commerce marketing funnels?", "Percentage of website visitors who complete a desired commercial action (e.g. purchase, registration)", "Conversion Rate Optimization"),
            ("What is Consumer Persona (Buyer Persona) profiling?", "Semi-fictional archetypes representing ideal customer demographics, psychographics, goals, pain points, and buying triggers", "Consumer Persona Research"),
            ("What does Omnichannel Marketing ensure across customer touchpoints?", "Seamless, consistent brand messaging and customer experience across physical retail stores, websites, and mobile apps", "Omnichannel Customer Journey"),
            ("In advertising ethics under the Advertising Standards Council of India (ASCI), what constitutes misleading advertising?", "Advertisements that deceive consumers through false claims, hidden disclaimers, or unsubstantiated performance statistics", "ASCI Advertising Ethics (India)"),
            ("What is 'Content Marketing'?", "Creating and distributing valuable, relevant, and consistent educational content to attract and retain an audience", "Content Marketing Strategy"),
            ("What does Net Promoter Score (NPS) measure in customer loyalty research?", "Customer willingness to recommend a brand to friends or colleagues on an 11-point index (Promoters minus Detractors)", "NPS Customer Advocacy")
        ]),
        ("company-secretary-cs", "Company Secretary (CS)", "corporate_secretarial_law", [
            ("Under the Indian Companies Act 2013, what is the primary statutory function of a Company Secretary?", "Ensure the company complies with statutory and regulatory legal provisions, managing board meetings and corporate governance", "Corporate Governance Statutory Role"),
            ("What is the quorum requirement for a Board of Directors meeting of a public company in India?", "One-third of total strength or two directors, whichever is higher (Companies Act Section 174)", "Board Governance Quorum"),
            ("What is Secretarial Audit mandated under Section 204 of the Indian Companies Act?", "Mandatory independent audit of company secretarial and legal records by a practicing CS for listed and large public firms", "Secretarial Audit Compliance"),
            ("In corporate law, what does the 'Doctrine of Ultra Vires' signify regarding actions of a company?", "Any transaction or action executed by a company beyond the powers granted in its Memorandum of Association is legally void", "Corporate Ultra Vires Doctrine"),
            ("What does SEBI's LODR Regulations mandate for publicly listed companies in India?", "Listing Obligations and Disclosure Requirements ensuring timely financial disclosure and governance compliance", "SEBI LODR Compliance (India)"),
            ("What is the maximum permissible gap between two consecutive Annual General Meetings (AGMs) under Companies Act 2013?", "Not more than 15 months, and held within 6 months of financial year close", "AGM Statutory Timelines"),
            ("What is the legal purpose of the Articles of Association (AOA) of a corporation?", "Governs internal operational management, director powers, voting rights, and share transfer rules of the company", "Memorandum & Articles of Association"),
            ("What is Insider Trading Prohibition enforced by SEBI in India?", "Prohibits trading in listed securities while possessing Unpublished Price Sensitive Information (UPSI)", "SEBI UPSI Insider Regulations"),
            ("What constitutes a 'Special Resolution' passed in a shareholders' general meeting?", "A resolution passed by minimum three-fourths (75%) majority votes cast by voting shareholders", "Shareholder Voting Thresholds"),
            ("What is the statutory role of the National Company Law Tribunal (NCLT) in India?", "Specialized quasi-judicial body adjudicating corporate disputes, company insolvency, mergers, and winding up", "NCLT & Insolvency Jurisprudence")
        ]),
        ("lawyer", "Lawyer", "jurisprudence_advocacy", [
            ("What is 'Stare Decisis' in common law legal systems?", "The legal doctrine requiring courts to adhere to settled historical precedent established in prior higher judicial decisions", "Legal Doctrine of Precedent"),
            ("Under Article 21 of the Indian Constitution, what fundamental right is guaranteed?", "Right to Protection of Life and Personal Liberty", "Indian Constitutional Law"),
            ("What is the burden of proof in criminal trials in India under the Indian Evidence Act?", "Beyond Reasonable Doubt (borne entirely by the prosecution)", "Criminal Burden of Proof"),
            ("What is a Writ of 'Habeas Corpus' issued by the Supreme Court (Art 32) or High Courts (Art 226)?", "A judicial order directing an authority detaining a person to produce the prisoner in court to justify lawful detention", "Constitutional Writ Jurisdiction"),
            ("In contract law, what constitutes 'Consideration' under the Indian Contract Act 1872?", "Something of value promised or exchanged between parties (quid pro quo); essential for a valid binding contract", "Contractual Consideration"),
            ("What is the difference between a Cognizable Offence and a Non-Cognizable Offence in CrPC?", "In cognizable offences, a police officer can arrest without an arrest warrant and begin immediate investigation", "Criminal Procedure Code (CrPC)"),
            ("What is Alternate Dispute Resolution (ADR) commonly utilized for?", "Resolving legal disputes outside formal court litigation via Arbitration, Conciliation, Mediation, and Lok Adalats", "Arbitration & Mediation (ADR)"),
            ("What ethical principle governs Advocate professional conduct under the Bar Council of India (BCI) Rules?", "An advocate must fearless uphold client interests through all fair and honorable means while maintaining absolute truth to court", "Bar Council of India Ethics"),
            ("What is a Public Interest Litigation (PIL) in Indian constitutional jurisprudence?", "Legal action initiated in courts for protection of public interest and marginalized groups by public-spirited citizens", "PIL Jurisprudence in India"),
            ("In tort law, what does the rule of 'Strict Liability' (Rylands v. Fletcher) enforce?", "Liability for damages caused by escape of hazardous substances brought onto land, regardless of absence of negligence", "Tort Law & Strict Liability")
        ]),
        ("ias-officer", "IAS Officer", "public_administration_policy", [
            ("In Indian district administration, what is the primary role of the District Collector / District Magistrate (IAS)?", "Heads district governance, maintenance of law & order, land revenue administration, and disaster coordination", "District Administration Governance"),
            ("What does the 73rd and 74th Constitutional Amendments mandate in Indian democratic governance?", "Panchayati Raj Institutions (rural local self-government) and Urban Local Bodies (municipalities)", "Decentralized Local Governance"),
            ("What is the statutory mechanism of the Right to Information (RTI) Act 2005?", "Empowers citizens to inspect government records, promoting transparency and bureaucratic accountability", "RTI & Administrative Transparency"),
            ("In disaster management, what role does the District Disaster Management Authority (DDMA) play under DM Act 2005?", "Coordinates multi-departmental emergency relief, hazard mitigation, rescue operations, and resource deployment", "Disaster Management Protocols"),
            ("What constitutional safeguard protects civil servants under Article 311 of the Indian Constitution?", "No civil servant can be dismissed or reduced in rank without an inquiry affording reasonable opportunity to be heard", "Civil Service Constitutional Safeguards"),
            ("What is the Public Distribution System (PDS) under the National Food Security Act 2013?", "Management of food grain procurement and distribution to eligible households at subsidized prices via fair price shops", "Welfare Scheme Implementation"),
            ("How does an IAS officer maintain ethical political neutrality during national and state elections?", "Enforce Election Commission of India Model Code of Conduct impartially as District Election Officer", "Election Administration & Neutrality"),
            ("What is the purpose of Citizen Charters in public service delivery?", "Public commitments specifying standards, quality, timeframes, and grievance redressal mechanisms of public services", "Citizen Charters & Public Accountability"),
            ("In policy evaluation, what is Cost-Benefit Analysis (CBA) of public infrastructure projects?", "Systematically weighing societal economic, environmental, and social benefits against public expenditure", "Public Policy Economic Analysis"),
            ("What does E-Governance (e.g. Digital India platforms) achieve in citizen public administration?", "Delivers public services digitally, eliminating bureaucratic rent-seeking, reducing delays, and increasing citizen access", "E-Governance Transformation")
        ]),
        ("ips-officer", "IPS Officer", "police_administration_law_order", [
            ("In criminal investigation, what is the legal significance of the First Information Report (FIR) under Section 154 CrPC?", "The earliest written recording of information regarding commission of a cognizable offence initiating police investigation", "Criminal Procedure FIR Mechanics"),
            ("What is the primary role of forensic ballistics in criminal homicide investigations?", "Analyze bullet trajectories, firearms markings, rifling striations, and gunshot residue on suspects", "Forensic Ballistics & Crime Scene"),
            ("In crowd and riot control, what does the principle of 'Minimum Force' mandate?", "Using only proportionate, necessary, and graduated force to disperse unlawful assemblies and restore public safety", "Police Crowd Control Protocols"),
            ("What does the Protection of Children from Sexual Offences (POCSO) Act mandate for police officers?", "Mandatory child-friendly reporting procedures, non-disclosure of victim identity, and expedited specialized investigation", "Specialized Child Protection Laws"),
            ("What constitutional right must an arresting police officer respect under Article 22(2) of the Indian Constitution?", "Produce the arrested person before the nearest judicial magistrate within 24 hours of arrest excluding travel time", "Constitutional Arrest Safeguards"),
            ("What is Cyber Crime Forensics in modern policing?", "Extracting, preserving, and analyzing digital evidence from hard drives, smartphones, and network server logs for court", "Digital Cyber Forensics"),
            ("What is Community Policing (e.g. Friends of Police, Janamaithri)?", "Building collaborative partnerships between local citizens and police stations to proactively prevent crime", "Community Policing Strategies"),
            ("In anti-narcotics enforcement under the NDPS Act 1985, what procedural compliance is critical during search and seizure?", "Ensuring presence of an independent gazetted officer or magistrate (Section 50) and strict chain of custody", "NDPS Act Search & Seizure"),
            ("What is the National Crime Records Bureau (NCRB)?", "Central governmental agency tracking, analyzing, and publishing annual crime statistics and coordinating fingerprint data", "National Crime Analytics"),
            ("During high-stress hostage negotiation or armed terrorism incidents, what is the primary operational priority?", "Neutralize threats with zero innocent civilian casualties while coordinating tactical and perimeter containment", "Counter-Terrorism & Hostage Rescue")
        ]),
        ("journalist", "Journalist", "journalism_mass_comm", [
            ("What is the 'Inverted Pyramid' structural style in news reporting?", "Placing the most crucial facts (Who, What, When, Where, Why) in the opening lead paragraph, followed by supporting details", "News Writing Structure"),
            ("What constitutes 'Defamation' under Section 499 of the Indian Penal Code?", "Making or publishing false imputations intending to harm the reputation of a person without verified public interest", "Media Law & Defamation"),
            ("What is the ethical principle of 'Right of Reply' in investigative reporting?", "Offering the person or institution accused of wrongdoing an adequate opportunity to respond before publication", "Journalistic Balance & Reply"),
            ("What is Yellow Journalism (Sensationalism)?", "Journalism that distorts facts with dramatic, unverified, or exaggerated headlines to attract viewership", "Media Ethics & Sensationalism"),
            ("What does 'On the Record' versus 'Off the Record' signify in journalistic interviews?", "'On the record' allows direct attribution by name; 'off the record' cannot be published or attributed directly", "Journalistic Attribution Rules"),
            ("What is Data Journalism?", "Using computational statistics, data scraping, and interactive visualizations to uncover stories in public datasets", "Data Journalism & Investigation"),
            ("What is the role of the Press Council of India (PCI)?", "Statutory quasi-judicial watchdog preserving freedom of the press and enforcing professional standards of journalistic ethics", "Press Council Standards (India)"),
            ("What is Citizen Journalism empowered by digital smartphones?", "Everyday citizens capturing, recording, and reporting live breaking news from public events directly to social media", "Participatory Digital Media"),
            ("What distinguishes an Editorial opinion column from an objective News Report?", "An editorial presents subjective analysis and policy stances of the newsroom; news reports strictly present verified facts", "Editorial vs Objective Reporting"),
            ("What is 'Sting Operation' jurisprudence in investigative media under Supreme Court guidelines?", "Permissible in public interest only when genuine societal harm is exposed without entrapping innocent individuals unlawfully", "Investigative Undercover Ethics")
        ]),
        ("psychologist", "Psychologist", "psychology_counseling", [
            ("What is Cognitive Behavioral Therapy (CBT) centered upon?", "Identifying and modifying maladaptive cognitive thought patterns and behavioral responses to alleviate distress", "Cognitive Behavioral Therapy (CBT)"),
            ("What is the primary manual published by the American Psychiatric Association for classifying mental health disorders?", "DSM-5 (Diagnostic and Statistical Manual of Mental Disorders)", "Psychiatric Diagnostic Systems"),
            ("What did Ivan Pavlov demonstrate through his famous experiments with dogs?", "Classical Conditioning (learned associations between neutral conditioned stimuli and biological unconditioned responses)", "Classical Conditioning Theory"),
            ("In psychometrics, what is the difference between Test Reliability and Test Validity?", "Reliability is consistency of measurement; validity is whether the test genuinely measures what it claims to measure", "Psychometric Test Standards"),
            ("What is the 'Fight or Flight' physiological stress response coordinated by?", "Sympathetic Nervous System and Hypothalamic-Pituitary-Adrenal (HPA) axis", "Neurobiology of Stress"),
            ("What did Jean Piaget's theory of cognitive development outline in children?", "Sequential stages of intellectual development: Sensorimotor, Preoperational, Concrete Operational, and Formal Operational", "Developmental Child Psychology"),
            ("What is 'Active Empathy' in Carl Rogers' Person-Centered Humanistic Therapy?", "Unconditional positive regard, genuine congruence, and accurate empathetic understanding of client subjective reality", "Humanistic Person-Centered Therapy"),
            ("What is Defense Mechanism in psychoanalytic theory (e.g. Rationalization, Projection)?", "Unconscious psychological strategies used to protect the ego from anxiety and unacceptable impulses", "Psychodynamic Defense Mechanisms"),
            ("What is the difference between a Clinical Psychologist and a Psychiatrist?", "Psychiatrists are medical doctors (MBBS + MD) licensed to prescribe pharmaceutical drugs; psychologists specialize in psychotherapy", "Psychology vs Psychiatry Roles"),
            ("In social psychology, what is the 'Bystander Effect' (Diffusion of Responsibility)?", "Individuals are less likely to offer help to a victim when other people are present", "Social Psychological Phenomena")
        ]),
        ("graphic-designer", "Graphic Designer", "graphic_visual_design", [
            ("What is the difference between Raster graphics and Vector graphics in digital design?", "Raster is composed of fixed pixels (JPEG/PNG) and pixelates when scaled; Vector is mathematical paths (SVG/AI) and scales infinitely", "Raster vs Vector Design"),
            ("What are 'Complementary Colors' on the traditional visual color wheel?", "Colors situated directly opposite each other on the color wheel (e.g. Blue and Orange), creating vibrant high-contrast pairings", "Color Theory & Contrast"),
            ("What is 'Kerning' in typography?", "Adjusting the horizontal spacing between specific individual letter pairs to achieve harmonious visual balance", "Typographic Kerning & Leading"),
            ("In UI/UX design, what is 'Visual Hierarchy' designed to accomplish?", "Arranging visual elements by scale, weight, and color to naturally guide the user's eye across the page in order of importance", "Visual Hierarchy Principles"),
            ("What does RGB color mode represent versus CMYK color mode?", "RGB is additive color for digital screens (Red, Green, Blue); CMYK is subtractive color for physical printing (Cyan, Magenta, Yellow, Black)", "Color Modes for Screen vs Print"),
            ("What is a 'Grid System' in editorial and layout design?", "An underlying structure of columns, gutters, and baselines that aligns content symmetrically and creates cohesive layout harmony", "Grid Systems & Layout Design"),
            ("What is the purpose of 'Wireframing' in digital product design?", "Creating low-fidelity structural blueprints of user interface layouts to map user flows before applying visual styling", "UI/UX Wireframing"),
            ("What is 'Serif' versus 'Sans-Serif' in typographic classification?", "Serif typefaces have decorative small strokes or feet on letter terminals (Times); Sans-Serif typefaces do not (Helvetica, SF Pro)", "Typographic Classification"),
            ("What is a Design System (e.g. Material Design, Apple HIG)?", "A unified collection of reusable components, design tokens, and style guidelines that standardize user interfaces across products", "Design Systems & Component Libraries"),
            ("In visual branding, what does a Brand Style Guide specify?", "Rules governing logo usage, minimum clear space, official color hex codes, typographic scales, and brand tone of voice", "Brand Guidelines & Governance")
        ]),
        ("fashion-designer", "Fashion Designer", "fashion_apparel_design", [
            ("What is 'Draping' in garment apparel design?", "Manipulating three-dimensional fabric directly on a dress form (mannequin) to create and visualize garment silhouette structure", "Garment Draping Techniques"),
            ("What is Haute Couture in the global fashion industry?", "High-end bespoke, custom-fitted high-fashion garments crafted by hand with luxury craftsmanship in Paris or fashion capitals", "Haute Couture vs Ready-to-Wear"),
            ("In textile science, what distinguishes Natural fibers from Synthetic fibers?", "Natural fibers come from plants/animals (Cotton, Silk, Wool); Synthetic fibers are chemical polymers (Polyester, Nylon, Spandex)", "Textile Fiber Science"),
            ("What is a 'Tech Pack' in apparel manufacturing production?", "Comprehensive specification document detailing garment measurements, bill of materials, stitch types, trims, and colorways for factories", "Technical Production Packages"),
            ("What does 'Fashion Trend Forecasting' analyze?", "Cultural, economic, sociological, and street movements to predict future colors, fabrics, silhouettes, and consumer apparel shifts", "Fashion Trend Forecasting"),
            ("What is 'Pattern Making' in fashion garment construction?", "Drafting flat 2D pattern templates from body measurements that are cut from fabric and assembled into a 3D garment", "Flat Pattern Drafting"),
            ("What is Sustainable / Circular Fashion aimed at achieving?", "Minimizing textile waste through upcycling, organic materials, non-toxic dyeing, and designing clothes to be recycled or biodegraded", "Sustainable Circular Fashion"),
            ("What does the 'Silhouette' of a garment refer to?", "The overall outer shape or outline contour that a garment creates when worn on the human body (e.g. A-line, Hourglass, Oversized)", "Garment Silhouette Analysis"),
            ("What is a 'Capsule Wardrobe' collection?", "A focused collection of versatile, interchangeable clothing items that can be recombined into numerous distinct outfits", "Capsule Apparel Collections"),
            ("In textile manufacturing, what is the difference between Woven fabrics and Knitted fabrics?", "Woven fabrics interlace warp and weft yarns at right angles; knitted fabrics interloop continuous yarn loops, providing inherent stretch", "Fabric Construction (Weaving vs Knitting)")
        ]),
        ("political-scientist", "Political Scientist", "political_science_geopolitics", [
            ("What did Montesquieu conceptualize in 'The Spirit of the Laws' regarding the Separation of Powers?", "Dividing state authority among Legislative, Executive, and Judicial branches with mutual checks and balances to prevent tyranny", "Separation of Powers Theory"),
            ("What does 'Sovereignty' signify in political science and international law?", "Supreme, independent authority of a state to govern its territory and people without external foreign interference", "Sovereignty & Statehood"),
            ("What distinguishes a Federal system of government from a Unitary system?", "Federal divides constitutional sovereignty between national and regional state governments (e.g. India); Unitary concentrates power centrally", "Federalism vs Unitary Governance"),
            ("In international relations theory, what is 'Realism' centered upon?", "States act as rational, self-interested sovereign actors in an anarchic global system, competing for national security and power", "International Relations Realism"),
            ("What is the difference between a First-Past-The-Post (FPTP) electoral system and Proportional Representation (PR)?", "FPTP awards victory to candidate with most votes in a district; PR allocates seats to parties based on overall national vote share percentage", "Comparative Electoral Systems"),
            ("What is 'Soft Power' as coined by political scientist Joseph Nye?", "A country's ability to influence others through culture, political values, and diplomatic foreign policies rather than military force", "Diplomatic Soft Power"),
            ("Under the Indian Constitution, what makes India a 'Secular' Republic?", "The state has no official state religion, treats all faiths equally, and guarantees freedom of conscience (Articles 25-28)", "Constitutional Secularism in India"),
            ("What does 'Bicameralism' mean in legislative architecture?", "A legislature composed of two separate houses or chambers (e.g. Lok Sabha and Rajya Sabha in Indian Parliament)", "Legislative Bicameralism"),
            ("What is 'Civil Society' in modern political theory?", "Non-governmental organizations, civic associations, and community groups operating independently of the state and market", "Civil Society & Democratic Pluralism"),
            ("What does the 'Social Contract Theory' (Hobbes, Locke, Rousseau) explore?", "The foundational consent of citizens to surrender certain natural freedoms to a sovereign state in exchange for protection of rights and order", "Social Contract Philosophy")
        ])
    ]

    for cslug, ctitle, topic, items in careers_data:
        for idx, (txt, answer, sk) in enumerate(items, 1):
            opts = [
                ("A", answer, 1.0, True),
                ("B", f"Opposite of {sk.lower()}", 0.0, False),
                ("C", f"Irrelevant administrative concept in {topic}", 0.0, False),
                ("D", "None of the above", 0.0, False)
            ]
            questions.append({
                "question_code": f"FIXED_{cslug.replace('-', '_').upper()[:12]}_{idx:03d}",
                "career_slug": cslug,
                "category": "domain_technical",
                "sub_topic": topic,
                "education_level": "all",
                "difficulty": "medium",
                "skill_name": sk,
                "text": txt,
                "question_type": "multiple_choice",
                "scoring_type": "accuracy",
                "explanation": f"{sk} represents core professional technical mastery required for {ctitle}.",
                "options": [{"option_key": o[0], "text": o[1], "score_value": o[2], "is_correct": o[3]} for o in opts]
            })

    return questions

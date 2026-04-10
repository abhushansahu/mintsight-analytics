Deep Dive: Customer Intent Analytics on Solana
Similar Projects (Hackathon Builders)
Note: These are hackathon submissions — demos and prototypes, not production products. Many may no longer be active. They're included as inspiration and to show what's been tried before, not as a competitive landscape.

Treso (treso, Cypherpunk, Sep 2025) — Marketing analytics platform predicting trends from real-world purchasing and behavioral data on Solana. The most directly overlapping concept to your idea: targets marketing agencies and brand managers with on-chain analytics + predictive modeling. No prize, no accelerator, team of 4. Low crowdedness score (123).

Crush (crush, Breakout, Apr 2025) — 2nd Place DePIN ($20K). Self-described "Hivemapper of consumer purchase data." Users upload shopping receipts for token rewards; advertisers buy aggregated shopper insights. Introduced a "proof of price" DePIN category. Receipt-scan based (not onchain-native), B2C advertising-focused. Solo founder.

Scanna (scanna, Cypherpunk, Sep 2025) — Honorable mention. Market research infrastructure providing real-time behavioral analytics via incentivized surveys. Targets the "$150B market research industry" with instant micropayments. Survey-based, not transaction-based.

Pine Analytics (pine-analytics, Cypherpunk, Sep 2025) — 4th Place Infrastructure ($10K). Real-time blockchain analytics with AI-readable data layer. General-purpose ("granular, queryable insight into the crypto economy"), not payment/commerce-specific.

CONYR (conyr, Breakout, Apr 2025) — 5th Place Infrastructure ($5K). Real-time AI intelligence engine with behavioral insights, adaptive clustering, anomaly detection. Focused on security and DeFi traders, not commerce analytics.

Solana Merchant AI (solana-merchant-ai, Cypherpunk, Sep 2025) — AI-powered POS for merchants with automated settlement, analytics, and customer insights. Customer analytics is a feature, not the core product. Team of 4.

MISK.FI (misk.fi, Cypherpunk, Sep 2025) — B2B stablecoin infrastructure for checkouts, subscriptions, multilateral netting, and on-chain receipts. Payment rails, not analytics — but its receipt data is exactly the kind of structured data your platform would consume.

Soliate (soliate, Radar, Sep 2024) — Automated Web3 marketing platform with transparent on-chain campaign tracking and performance analytics. Marketing performance tracking, not transaction/payment analytics.

Archive Insights
a16z, "Tourists in the Bazaar" (Sam Broner, Feb 2026) — Argues AI agents will behave like businesses, not tourists: pre-negotiated vendor relationships, volume pricing, net-30 invoices. Two payment relationships emerge (user→agent, agent→vendor) requiring B2B payment intelligence. Credit cards are "bad technology fit for agents." This validates the thesis that B2B payment flows will need a new intelligence layer — someone needs to make those flows legible. (source)

Galaxy Research, "The Future of Payments" (Apr 2025) — Stablecoins represent ~60% of onchain transaction value despite being a fraction of crypto market cap. Cross-border payments identified as "first battleground." The volume is there; the intelligence layer is not. (source)

Galaxy Research, "Agentic Payments" (Jan 2026) — Incumbents already experimenting with stablecoins alongside agentic payment capabilities. "Onchain settlement will increasingly coexist with traditional payment infrastructure." The open question is who captures the intelligence layer on top. (source)

Alliance DAO, "Fintech RFS" (Feb 2026) — Identifies "superior credit underwriting using unstructured data" and "agentic backend workflows driving cost-to-serve near zero" as key technology unlocks. Explicitly flags that "Shopping is Dead, AI is Taking Over" — payment networks are building infrastructure while AI platforms deploy, creating startup opportunities in "vertical specialization and merchant tools." (source)

Arxiv, "Ethereum Fraud Detection via Joint Transaction Language Model" (Sep 2024) — Academic work on using deep multi-head attention networks to fuse transaction semantic and similarity embeddings for account-level intelligence. Demonstrates that onchain transaction graph data can be structured into meaningful behavioral embeddings — the same approach applicable to commerce intent rather than fraud detection. (source)

Current Landscape
Angle 1: Transaction Data Enrichment (The "Onchain Spade")
Key players: Spade ($40M Series B, Mar 2026) is the Web2 category leader processing 1.9B transactions/day with 99.9% merchant coverage. Partners with Stripe and Bilt. 470% YoY revenue growth. No blockchain version exists. Plaid (acquired by Visa attempt at $5.3B) pioneered the financial data API model. Bud Financial offers transaction enrichment for banks (build-or-buy positioning).
Recent developments: Transaction enrichment platform market valued at $2.15B (2024), growing at 16.8% CAGR to $9B by 2033. Payment data enrichment market specifically at $1.62-1.72B growing at 21-22% CAGR.
On Solana: Grid keyword search for "payment analytics" returned zero results. No productized payment enrichment product exists on Solana. Helius offers raw transaction indexing (Enhanced Transactions API, LaserStream) and Vybe provides DeFi analytics, but neither enriches payment transactions with merchant identity, product categories, or commerce intent.
Maturity: Open space on-chain / Established off-chain. The gap between off-chain sophistication and on-chain absence is the opportunity.
Angle 2: B2B Commerce Intelligence on Stablecoin Rails
Key players: B2B stablecoin payments surged 730% YoY in 2025, reaching $3B/month by early 2026. Solana processed $1T+ in stablecoin volume in 2025. CargoBill (C3 accelerator, 1st place Stablecoins), MISK.FI, and LINK Business are building B2B payment rails — none offer analytics on those flows.
Recent developments: Solana launched payments.org (Feb 2026) with Visa, PayPal, and Western Union integrations. Western Union issuing USDPT stablecoin on Solana targeting 500,000+ retail agents. Fiserv issuing FIUSD targeting 10,000 financial institutions. B2B now represents ~60% of total stablecoin payment activity.
Intelligence gap: Enterprises using stablecoins for cross-border supplier payments, marketplace settlements, and inter-subsidiary transfers have no structured way to understand their counterparty spending patterns, product demand signals, or competitive positioning.
Maturity: Emerging. B2B stablecoin rails are growing explosively but the intelligence layer is nonexistent.
Angle 3: Consumer Purchase Data Layer
Key players: Crush (2nd place DePIN, Breakout) demonstrated demand for consumer purchase data with receipt-scan DePIN model. Scanna (Honorable mention, Cypherpunk) uses incentivized surveys. Nansen labels 300M+ wallet addresses but for DeFi/trading, not commerce. Chainalysis introduced "blockchain intelligence agents" (2026) but for compliance, not commerce.
Incumbents off-chain: Nielsen, IRI/Circana, and Bloomberg Second Measure all provide consumer purchase intelligence. None operate on blockchain data.
On Solana: Bannga (bannga, Cypherpunk) converts consumer spending into crypto rewards. Tagacy (tagacy, Renaissance) mints NFTs for transaction receipts. Both capture consumer spending moments but don't aggregate or analyze them.
Maturity: Emerging. Consumer-side is harder because onchain consumer payment volume is smaller than B2B, but growing fast (USDC on Solana surpassed Ethereum in late 2025).
Key Insights
Patterns: Payment rails are proliferating on Solana (25+ on/off ramps, multiple POS systems, B2B settlement platforms) but intelligence follows infrastructure — and the intelligence layer hasn't been built yet. This mirrors the Web2 pattern where Stripe/Plaid/Square created the rails and Spade/Ramp/Bud built the analytics on top.

Gaps: The specific intersection of "onchain payment data" + "merchant/provider identity" + "customer intent intelligence" has zero products in The Grid's 6,300+ product database and no hackathon winner has directly addressed it. Tag-filtered searches for "fragmented marketing data" returned only 2 projects; "lack of consumer data ownership" returned 1 project (Crush). This is genuinely underexplored.

Trends: The a16z thesis ("agents will behave like businesses") and Alliance DAO's "Shopping is Dead, AI is Taking Over" both point to the same conclusion: AI agents will generate massive B2B payment volume that needs to be made legible. The agent-to-agent payment economy will need transaction intelligence from Day 1 — there's no legacy Spade-equivalent to rely on.

Hackathon distribution: Across 5,428 projects and 293 winners, "Consumer Apps" is the most common track (~20% share) but problemTags like "fragmented liquidity" (120), "information overload" (87), and "high platform fees" (68) dominate — none of the top 10 problem tags relate to payment/commerce intelligence. This is a true whitespace.

Opportunities & Gaps
Primary opportunity — "The Onchain Spade": Transaction data enrichment for Solana payment flows. $2.15B market off-chain growing to $9B by 2033. Zero on-chain competitors. Spade's 470% revenue growth validates demand. The building blocks (Helius raw indexing, stablecoin payment rails) exist; the intelligence layer does not.

Secondary opportunity — B2B Payment Intelligence: As B2B stablecoin payments hit $3B/month, enterprises need to understand counterparty spending patterns. Could start as a feature within the primary opportunity, focused on supply chain and cross-border B2B flows.

Tertiary opportunity — Agent Commerce Analytics: As AI agents generate payment volume (per a16z thesis), agent-to-agent transaction intelligence will be a new category. Early-mover advantage possible by building the labeling/enrichment layer now before agent payment volume scales.

Deep Dive: The Onchain Spade — Transaction Data Enrichment for Solana Payment Flows
Market Landscape
Who are the key players?

Spade (Web2, $40M Series B): Enriches card/ACH/wire data with merchant identity, category, location. 1.9B tx/day, 99.9% U.S./Canadian merchant coverage. Partners: Stripe, Bilt. Revenue growing 470% YoY.
Bud Financial (Web2): Transaction enrichment for banks, positioned as build-vs-buy decision for FIs.
Helius (Solana): Raw transaction indexing and streaming. Enhanced Transactions API provides parsed instruction data, but no merchant identity enrichment or commerce categorization. Grid rank score: not payment-analytics-specific.
Vybe Network (Solana, Grid product ID 51): DeFi analytics API — token transfers, DEX data, pricing. Not commerce-oriented.
Nansen (Multi-chain): 300M+ labeled addresses, smart money tracking. Labels are DeFi/trading-oriented (whale wallets, exchange wallets), not commerce entities.
Top Ledger (Solana, Grid product ID 1456): Analytics platform for Solana. General protocol analytics, not payment enrichment.
Landscape classification: Open space. Based on the available data, no existing player offers productized payment commerce analytics or transaction enrichment on Solana — or on any blockchain. Grid keyword search for "payment analytics" returned 0 products. The 326 products across payment infrastructure + data API categories on Solana (251 distinct roots) are all either payment rails (moving money) or raw data infrastructure (indexing blocks/transactions). None sits in the middle as an intelligence layer enriching what those transactions mean commercially.

Evidence: Grid saturation check shows 326 products / 251 roots across payment infra + data APIs on Solana, but the payment analytics intersection is empty. Spade's $40M raise and 470% growth off-chain prove the business model works. The transaction enrichment platform market is $2.15B growing to $9B.

The Problem
What is the concrete friction? A Solana-native business (e.g., a stablecoin payment processor like CargoBill, or a merchant using Decal's POS) receives stablecoin payments but sees raw transaction hashes, not structured commercial data. They can't answer: "Which product categories are driving revenue growth?", "What's our customer retention by segment?", "How does our spending pattern compare to competitors in our vertical?" — all questions trivially answered in traditional finance through Spade/Plaid. The same problem exists for investors, analysts, and AI agents trying to understand the onchain commerce economy.

Who experiences this pain? Three personas: (1) Stablecoin payment platforms (CargoBill, Decal, LocalPay, MISK.FI) who want to offer analytics to their merchants. (2) Enterprises/treasuries making B2B payments via stablecoins who need spend intelligence and counterparty analysis. (3) Investors and analysts trying to understand onchain commerce trends, merchant health, and product demand signals.

How do they solve it today? Manually. Teams export transaction CSVs, cross-reference wallet addresses with known entities, and build internal dashboards. TRES Finance (Grid product ID 767) offers a "Financial Data Lake" for protocol-level accounting but not merchant-level intelligence. Dune dashboards can be built for specific protocols but there's no productized enrichment API.

What's the quantified impact? Solana processed $1T+ in stablecoin volume in 2025. B2B stablecoin payments alone hit $3B/month by early 2026 (730% YoY growth). Even capturing 0.1% of Solana stablecoin volume for enrichment at a $0.001/tx API fee on 116B annual transactions represents a significant revenue opportunity. The off-chain market is $2.15B today, growing at 16.8% CAGR.

Revenue Model
How does this make money? API-based pricing, mirroring Spade's model:

Per-transaction enrichment fee: $0.001-0.01 per transaction enriched (merchant identification, category, product classification)
Subscription tiers: Free tier (100K tx/month) → Growth ($250-500/month) → Enterprise (custom pricing) for dashboard access and bulk enrichment
Data licensing: Aggregated, anonymized commerce intelligence sold to investors, market researchers, and protocol teams (similar to how Bloomberg Second Measure sells anonymized credit card data)
Unit economics: Spade processes 1.9B tx/day and raised at implied $200M+ valuation. Gross margins in data enrichment APIs are typically 70-85% after initial labeling investment. The labeling cost is the major upfront investment — but onchain data is public and parseable, reducing the data acquisition cost versus Spade's card network partnerships.

TAM calculation: Transaction enrichment platform market: $2.15B (2024) → $9B (2033). Crypto/onchain slice: Solana stablecoin volume $1T+ annually. If 5% of that volume represents "real commerce" ($50B) and enrichment captures $0.002/tx on an estimated 500M commerce transactions/year = $1M/year just on Solana at current volume. With 730% B2B growth rates and multi-chain expansion, realistic 3-year addressable market: $10-50M ARR.

Comparable business models: Spade (transaction enrichment API, $40M raised), Plaid (financial data API, attempted $5.3B acquisition), Nansen (labeled wallet intelligence, $75M raised), Chainalysis (blockchain analytics, $6.5B+ valuation). All API-first, usage-based pricing with enterprise tiers.

Go-to-Market Friction
Is this a two-sided marketplace? Partially. You need (1) a labeling/enrichment engine (supply side: mapping wallet addresses to merchant/provider identities) and (2) customers who query that data (demand side). But unlike a pure marketplace, you can be your own supply side by building the labeling layer yourself using public onchain data + off-chain mapping.

Cold start problem: The hardest part is building the initial merchant identity database — mapping Solana wallet addresses to verified business entities with product/category classifications. Without this, the enrichment API returns nothing useful.

Bootstrap strategies:

Be the supply side yourself. Start by manually labeling the top 500-1,000 Solana merchant wallets using public data: Solana Pay integrations, payment protocol contract addresses, known merchant wallets from CargoBill/Decal/LocalPay/MISK.FI ecosystems. This is analogous to Nansen's early approach of manually labeling whale wallets.
Anchor customer strategy. Partner with one Solana payment platform (e.g., Decal, which is in C3 accelerator and has merchant relationships) to be their analytics backend. Their merchants become your first labeled entities, and their transaction volume becomes your first enrichment dataset.
Start in a niche vertical. Focus on one vertical first — stablecoin B2B payments in supply chain (CargoBill's domain) or retail POS (Decal's domain). Depth over breadth.
Open-source the labeling layer. Create a community-driven entity labeling system (like Arkham's Intel Exchange but for commerce entities) where contributors earn rewards for verified merchant labels. Crush's "proof of price" DePIN model could inform this.
Network effects: Moderate but positive. Each new merchant labeled increases the value of the enrichment API for all customers. Each new customer querying the API provides signal on which entities need labeling, creating a feedback loop. Strongest lock-in comes from enterprise customers building workflows on top of the API.

Founder-Market Fit
Ideal founder background: Someone who has worked at Spade, Plaid, Nansen, or Chainalysis — understanding both the data enrichment product model and the onchain data stack. Alternatively: a fintech product person with experience at a payment processor (Stripe, Adyen, Square) who understands merchant intelligence from the buyer's perspective, combined with Solana engineering depth.

What they bring: Understanding of how transaction enrichment creates value for financial institutions, pre-existing relationships with Solana payment companies (CargoBill, Decal, Sphere), and the ability to build and maintain a high-accuracy entity labeling system. Credibility with payment platform partners is critical for the anchor customer strategy.

Red flags: Pure crypto-native builders with no fintech/payments experience (they'll underestimate the difficulty of entity labeling and commercial data quality). Pure data scientists with no GTM instinct (the product needs to be sold to enterprise customers, not just built).

Team composition: Ideal trio: (1) Product/GTM lead with fintech or payments background, (2) Solana engineer who understands indexing, geyser plugins, and transaction parsing at scale, (3) Data engineer who can build and maintain the entity labeling pipeline.

Why Crypto/Solana?
What does blockchain specifically enable? Onchain transaction data is public, real-time, and permissionlessly accessible — no need for card network partnerships (Spade's moat) or bank data-sharing agreements (Plaid's moat). This fundamentally lowers the data acquisition cost. Additionally, stablecoin-denominated commerce provides clean, USD-denominated transaction values without the currency conversion noise of multi-currency card networks.

Could this be built without crypto? It already has been — Spade is a $40M-funded company doing this off-chain. The crypto version is differentiated by (1) open data access removing the moat of data partnerships, (2) real-time settlement data rather than T+1/T+2 batch data, (3) composability with other onchain protocols (DeFi, credit, lending can directly consume enriched payment data), and (4) the emerging agent-to-agent payment economy that will be crypto-native from Day 1.

Why Solana specifically? Highest stablecoin transaction volume surpassing Ethereum by late 2025. 400ms slot times enabling real-time enrichment. payments.org consortium with Visa/PayPal/Western Union. Helius and Vybe provide the raw data infrastructure to build on. Deepest ecosystem of payment-focused builders (CargoBill, Decal, LocalPay, Borderless Wallets — all C3 accelerator companies).

Risk Assessment
Technical risk: Medium. Core transaction parsing and indexing technology is proven (Helius, Vybe). The hard technical problem is entity labeling at scale with high accuracy — maintaining a continuously updated mapping of wallet addresses to verified business entities. Accuracy below 95% makes the product unreliable; Spade achieves 99%+ off-chain.

Regulatory risk: Low-Medium. Transaction data enrichment for analytics is lower-risk than compliance/AML (Chainalysis's domain). However, aggregating spending patterns could raise privacy concerns under GDPR/CCPA if any identifiable consumer data is included. Anonymization and aggregation are necessary defaults.

Market risk: Medium. This is a "painkiller" for payment platforms and analysts once onchain commerce volume is significant, but a "vitamin" at current scale. The bet is on onchain commerce volume continuing its explosive growth trajectory (730% YoY for B2B stablecoins). If stablecoin commerce stalls at current levels, the TAM may be too small. If Visa/PayPal/Western Union on Solana succeed, the TAM explodes.

Execution risk: High on labeling, low on infra. The entity labeling challenge is the make-or-break execution risk. Building a high-accuracy, high-coverage merchant identity database for onchain addresses is labor-intensive initially. Nansen took years to label 300M+ addresses. The advantage: commerce entities are fewer in number and more identifiable than DeFi wallets — merchant POS addresses are relatively stable and often publicly advertised.

Appendix: Further Reading
Study Spade's model closely — their blog and Stripe partnership announcement detail how transaction enrichment creates value for payment platforms
Crush (crush) — study the "proof of price" DePIN model for consumer data collection; their Breakout submission shows the receipt-scan architecture
Helius Enhanced Transactions API — the raw data building block; understand what enrichment they already provide and where the gap to commerce-level intelligence sits
a16z "Tourists in the Bazaar" — required reading on why B2B payment intelligence will be critical in the agent economy (full article)
Solana payments.org — understand the institutional payment consortium forming on Solana; these are your future data sources and potential customers (coverage)
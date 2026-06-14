/**
 * TrendWise AI — Stock Autocomplete
 * Provides ticker suggestions for Indian (NSE/BSE) + US stocks.
 */

const STOCK_DATABASE = [
  // ── Indian NSE Stocks ──────────────────────────
  { ticker: "RELIANCE.NS",  name: "Reliance Industries",    market: "NSE" },
  { ticker: "TCS.NS",       name: "Tata Consultancy Services", market: "NSE" },
  { ticker: "INFY.NS",      name: "Infosys",                market: "NSE" },
  { ticker: "HDFCBANK.NS",  name: "HDFC Bank",              market: "NSE" },
  { ticker: "ICICIBANK.NS", name: "ICICI Bank",             market: "NSE" },
  { ticker: "HINDUNILVR.NS",name: "Hindustan Unilever",     market: "NSE" },
  { ticker: "SBIN.NS",      name: "State Bank of India",    market: "NSE" },
  { ticker: "BHARTIARTL.NS",name: "Bharti Airtel",          market: "NSE" },
  { ticker: "ITC.NS",       name: "ITC Limited",            market: "NSE" },
  { ticker: "KOTAKBANK.NS", name: "Kotak Mahindra Bank",    market: "NSE" },
  { ticker: "LT.NS",        name: "Larsen & Toubro",        market: "NSE" },
  { ticker: "HCLTECH.NS",   name: "HCL Technologies",       market: "NSE" },
  { ticker: "AXISBANK.NS",  name: "Axis Bank",              market: "NSE" },
  { ticker: "ASIANPAINT.NS",name: "Asian Paints",           market: "NSE" },
  { ticker: "MARUTI.NS",    name: "Maruti Suzuki",          market: "NSE" },
  { ticker: "SUNPHARMA.NS", name: "Sun Pharmaceutical",     market: "NSE" },
  { ticker: "TITAN.NS",     name: "Titan Company",          market: "NSE" },
  { ticker: "BAJFINANCE.NS",name: "Bajaj Finance",          market: "NSE" },
  { ticker: "WIPRO.NS",     name: "Wipro",                  market: "NSE" },
  { ticker: "TATAMOTORS.NS",name: "Tata Motors",            market: "NSE" },
  { ticker: "ULTRACEMCO.NS",name: "UltraTech Cement",       market: "NSE" },
  { ticker: "ONGC.NS",      name: "Oil & Natural Gas Corp", market: "NSE" },
  { ticker: "NTPC.NS",      name: "NTPC Limited",           market: "NSE" },
  { ticker: "POWERGRID.NS", name: "Power Grid Corp",        market: "NSE" },
  { ticker: "TATASTEEL.NS", name: "Tata Steel",             market: "NSE" },
  { ticker: "ADANIENT.NS",  name: "Adani Enterprises",      market: "NSE" },
  { ticker: "ADANIPORTS.NS",name: "Adani Ports",            market: "NSE" },
  { ticker: "JSWSTEEL.NS",  name: "JSW Steel",              market: "NSE" },
  { ticker: "TECHM.NS",     name: "Tech Mahindra",          market: "NSE" },
  { ticker: "INDUSINDBK.NS",name: "IndusInd Bank",          market: "NSE" },
  { ticker: "BAJAJFINSV.NS",name: "Bajaj Finserv",          market: "NSE" },
  { ticker: "HDFCLIFE.NS",  name: "HDFC Life Insurance",    market: "NSE" },
  { ticker: "DIVISLAB.NS",  name: "Divi's Laboratories",    market: "NSE" },
  { ticker: "DRREDDY.NS",   name: "Dr. Reddy's Labs",       market: "NSE" },
  { ticker: "CIPLA.NS",     name: "Cipla",                  market: "NSE" },
  { ticker: "EICHERMOT.NS", name: "Eicher Motors",          market: "NSE" },
  { ticker: "BPCL.NS",      name: "Bharat Petroleum",       market: "NSE" },
  { ticker: "HEROMOTOCO.NS",name: "Hero MotoCorp",          market: "NSE" },
  { ticker: "COALINDIA.NS", name: "Coal India",             market: "NSE" },
  { ticker: "GRASIM.NS",    name: "Grasim Industries",      market: "NSE" },
  { ticker: "APOLLOHOSP.NS",name: "Apollo Hospitals",       market: "NSE" },
  { ticker: "NESTLEIND.NS", name: "Nestle India",           market: "NSE" },
  { ticker: "BRITANNIA.NS", name: "Britannia Industries",   market: "NSE" },
  { ticker: "TATACONSUM.NS",name: "Tata Consumer Products", market: "NSE" },
  { ticker: "SBILIFE.NS",   name: "SBI Life Insurance",     market: "NSE" },
  { ticker: "PIDILITIND.NS",name: "Pidilite Industries",    market: "NSE" },
  { ticker: "BAJAJ-AUTO.NS",name: "Bajaj Auto",             market: "NSE" },
  { ticker: "ZOMATO.NS",    name: "Zomato",                 market: "NSE" },
  { ticker: "PAYTM.NS",     name: "Paytm (One97 Comm.)",   market: "NSE" },
  { ticker: "IRCTC.NS",     name: "IRCTC",                  market: "NSE" },

  // ── Indian BSE Stocks (selected) ───────────────
  { ticker: "RELIANCE.BO",  name: "Reliance Industries",    market: "BSE" },
  { ticker: "TCS.BO",       name: "Tata Consultancy Services", market: "BSE" },
  { ticker: "INFY.BO",      name: "Infosys",                market: "BSE" },

  // ── US Stocks ──────────────────────────────────
  { ticker: "AAPL",    name: "Apple Inc.",              market: "NASDAQ" },
  { ticker: "MSFT",    name: "Microsoft Corporation",   market: "NASDAQ" },
  { ticker: "GOOGL",   name: "Alphabet (Google)",       market: "NASDAQ" },
  { ticker: "AMZN",    name: "Amazon.com",              market: "NASDAQ" },
  { ticker: "TSLA",    name: "Tesla Inc.",              market: "NASDAQ" },
  { ticker: "META",    name: "Meta Platforms",          market: "NASDAQ" },
  { ticker: "NVDA",    name: "NVIDIA Corporation",      market: "NASDAQ" },
  { ticker: "JPM",     name: "JPMorgan Chase",          market: "NYSE" },
  { ticker: "V",       name: "Visa Inc.",               market: "NYSE" },
  { ticker: "JNJ",     name: "Johnson & Johnson",       market: "NYSE" },
  { ticker: "WMT",     name: "Walmart Inc.",            market: "NYSE" },
  { ticker: "PG",      name: "Procter & Gamble",        market: "NYSE" },
  { ticker: "MA",      name: "Mastercard Inc.",          market: "NYSE" },
  { ticker: "DIS",     name: "Walt Disney Co.",          market: "NYSE" },
  { ticker: "NFLX",    name: "Netflix Inc.",             market: "NASDAQ" },
  { ticker: "PYPL",    name: "PayPal Holdings",          market: "NASDAQ" },
  { ticker: "INTC",    name: "Intel Corporation",        market: "NASDAQ" },
  { ticker: "AMD",     name: "Advanced Micro Devices",   market: "NASDAQ" },
  { ticker: "CRM",     name: "Salesforce Inc.",          market: "NYSE" },
  { ticker: "BA",      name: "Boeing Company",           market: "NYSE" },
  { ticker: "UBER",    name: "Uber Technologies",        market: "NYSE" },
  { ticker: "COIN",    name: "Coinbase Global",          market: "NASDAQ" },
  { ticker: "SNOW",    name: "Snowflake Inc.",            market: "NYSE" },
  { ticker: "SQ",      name: "Block Inc. (Square)",       market: "NYSE" },
  { ticker: "SPOT",    name: "Spotify Technology",        market: "NYSE" },
];


/**
 * Initialize autocomplete on a stock input field.
 * @param {string} inputId - The ID of the input element
 */
function initStockAutocomplete(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;

  // Create dropdown container
  const wrapper = document.createElement('div');
  wrapper.style.position = 'relative';
  input.parentNode.insertBefore(wrapper, input);
  wrapper.appendChild(input);

  const dropdown = document.createElement('div');
  dropdown.className = 'autocomplete-dropdown';
  dropdown.style.cssText = `
    position: absolute; top: 100%; left: 0; right: 0; z-index: 1050;
    max-height: 260px; overflow-y: auto; display: none;
    background: #fff; border: 1px solid #e0e3eb; border-top: none;
    border-radius: 0 0 6px 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  `;
  wrapper.appendChild(dropdown);

  let selectedIndex = -1;

  input.addEventListener('input', function () {
    const query = this.value.trim().toLowerCase();
    dropdown.innerHTML = '';
    selectedIndex = -1;

    if (query.length < 1) {
      dropdown.style.display = 'none';
      return;
    }

    const matches = STOCK_DATABASE.filter(s =>
      s.ticker.toLowerCase().includes(query) ||
      s.name.toLowerCase().includes(query)
    ).slice(0, 10);

    if (matches.length === 0) {
      dropdown.style.display = 'none';
      return;
    }

    matches.forEach((stock, idx) => {
      const item = document.createElement('div');
      item.className = 'autocomplete-item';
      item.dataset.index = idx;
      item.style.cssText = `
        padding: 10px 14px; cursor: pointer; display: flex;
        justify-content: space-between; align-items: center;
        border-bottom: 1px solid #f0f2f5;
      `;
      item.innerHTML = `
        <div>
          <strong style="color:#1a1a2e;">${stock.ticker}</strong>
          <span style="color:#6b7280; margin-left:8px; font-size:13px;">${stock.name}</span>
        </div>
        <span style="font-size:11px; padding:2px 8px; border-radius:4px;
          background:${stock.market === 'NSE' ? '#d1fae5' : stock.market === 'BSE' ? '#fef3c7' : '#dbeafe'};
          color:${stock.market === 'NSE' ? '#065f46' : stock.market === 'BSE' ? '#92400e' : '#1e40af'};">
          ${stock.market}
        </span>
      `;

      item.addEventListener('mouseenter', () => {
        item.style.background = '#f0fdf4';
      });
      item.addEventListener('mouseleave', () => {
        item.style.background = '';
      });
      item.addEventListener('click', () => {
        input.value = stock.ticker;
        dropdown.style.display = 'none';
        input.focus();
      });

      dropdown.appendChild(item);
    });

    dropdown.style.display = 'block';
  });

  // Keyboard navigation
  input.addEventListener('keydown', function (e) {
    const items = dropdown.querySelectorAll('.autocomplete-item');
    if (!items.length || dropdown.style.display === 'none') return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
      _highlightItem(items, selectedIndex);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, 0);
      _highlightItem(items, selectedIndex);
    } else if (e.key === 'Enter' && selectedIndex >= 0) {
      e.preventDefault();
      items[selectedIndex].click();
    } else if (e.key === 'Escape') {
      dropdown.style.display = 'none';
    }
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', function (e) {
    if (!wrapper.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });
}

function _highlightItem(items, index) {
  items.forEach((item, i) => {
    item.style.background = i === index ? '#f0fdf4' : '';
  });
  if (items[index]) items[index].scrollIntoView({ block: 'nearest' });
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', function () {
  // Try common input IDs used across pages
  ['stockName', 'sentimentTicker', 'insightsTicker'].forEach(id => {
    initStockAutocomplete(id);
  });
});

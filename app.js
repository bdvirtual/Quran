const surahHeader = document.getElementById("surahHeader");
const ayahContainer = document.getElementById("ayahContainer");

const surahSelectTop = document.getElementById("surahSelectTop");

const toggleArabic = document.getElementById("toggleArabic");
const toggleBn = document.getElementById("toggleBn");
const toggleW2W = document.getElementById("toggleW2W");

const backBtn = document.getElementById("backBtn");
const readingModeBtn = document.getElementById("readingModeBtn");
const settingsBtn = document.getElementById("settingsBtn");
const settingsDrawer = document.getElementById("settingsDrawer");
const drawerOverlay = document.getElementById("drawerOverlay");
const closeDrawerBtn = document.getElementById("closeDrawerBtn");

let metaData = null;
let currentSurah = null;

async function loadMeta() {
  const res = await fetch("./meta.json");
  metaData = await res.json();

  surahSelectTop.innerHTML = "";

  metaData.surahs.forEach((surah) => {
    const option = document.createElement("option");
    option.value = surah.surah_no;
    option.textContent = `${surah.surah_no} - ${surah.bn_name}`;
    surahSelectTop.appendChild(option);
  });
}

async function loadSurah(surahNo) {
  const res = await fetch(`./surahs/${surahNo}.json`);
  currentSurah = await res.json();
  renderSurah();
}

function renderSurah() {
  if (!currentSurah) return;

  surahSelectTop.value = currentSurah.surah_no;

  surahHeader.innerHTML = `
    <h2>${currentSurah.ar_name}</h2>
    <p>${currentSurah.bn_name}</p>
  `;

  ayahContainer.innerHTML = "";

  currentSurah.ayahs.forEach((ayah) => {
    const block = document.createElement("div");
    block.className = "ayah-block";

    let html = `
      <div class="ayah-meta">
        <span class="ayah-no">${ayah.ayah_no}</span>
        <span class="ayah-menu">⋯</span>
      </div>
    `;

    if (toggleArabic.checked) {
      html += `<div class="ayah-ar">${ayah.arabic}</div>`;
    }

    if (toggleW2W.checked && Array.isArray(ayah.words)) {
      html += `<div class="word-row">`;

      ayah.words.forEach((word) => {
        html += `
          <div class="word-cell">
            <div class="word-ar">${word.ar}</div>
            <div class="word-bn">${word.bn}</div>
          </div>
        `;
      });

      html += `</div>`;
    }

    if (toggleBn.checked) {
      html += `<div class="ayah-bn">${ayah.bn}</div>`;
    }

    block.innerHTML = html;

    block.addEventListener("click", () => {
      document.querySelectorAll(".ayah-block").forEach((item) => {
        item.classList.remove("active");
      });
      block.classList.add("active");
    });

    ayahContainer.appendChild(block);
  });

  if (!currentSurah.ayahs || currentSurah.ayahs.length === 0) {
    ayahContainer.innerHTML = `<div class="empty-note">এই সূরায় এখনো কোনো আয়াত লোড হয়নি।</div>`;
  }
}

function openDrawer() {
  settingsDrawer.classList.remove("hidden");
  drawerOverlay.classList.remove("hidden");
}

function closeDrawer() {
  settingsDrawer.classList.add("hidden");
  drawerOverlay.classList.add("hidden");
}

function bindEvents() {
  surahSelectTop.addEventListener("change", () => {
    loadSurah(surahSelectTop.value);
  });

  toggleArabic.addEventListener("change", renderSurah);
  toggleBn.addEventListener("change", renderSurah);
  toggleW2W.addEventListener("change", renderSurah);

  backBtn.addEventListener("click", () => {
    window.history.back();
  });

  readingModeBtn.addEventListener("click", () => {
    toggleBn.checked = !toggleBn.checked;
    renderSurah();
  });

  settingsBtn.addEventListener("click", openDrawer);
  closeDrawerBtn.addEventListener("click", closeDrawer);
  drawerOverlay.addEventListener("click", closeDrawer);
}

async function init() {
  await loadMeta();
  bindEvents();
  await loadSurah(100);
}

init();
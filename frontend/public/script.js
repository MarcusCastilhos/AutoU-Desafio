const API_BASE_URL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://autou-desafio-production.up.railway.app";

const analyzeBtn = document.getElementById("analyzeBtn");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const emailText = document.getElementById("emailText");
const responseDiv = document.getElementById("response");
const historyDiv = document.getElementById("history");

let history = [];
let openIndex = null;
let uploadedFileContent = "";
let isProcessingPDF = false;

fileInput.addEventListener("change", async () => {
  if (!fileInput.files.length) {
    fileName.textContent = "Nenhum arquivo selecionado";
    fileName.className = "";
    emailText.disabled = false;
    uploadedFileContent = "";
    return;
  }

  const file = fileInput.files[0];
  fileName.textContent = file.name;

  emailText.value = "";
  emailText.disabled = true;

  const isTXT =
    file.type === "text/plain" || file.name.toLowerCase().endsWith(".txt");
  const isPDF =
    file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");

  if (isTXT) {
    fileName.className = "ready";
    const reader = new FileReader();
    reader.onload = () => {
      uploadedFileContent = reader.result;
    };
    reader.readAsText(file);
  } else if (isPDF) {
    fileName.className = "processing";
    fileName.textContent = `${file.name} (extraindo texto...)`;
    isProcessingPDF = true;

    try {
      uploadedFileContent = await extractPDFText(file);
      fileName.className = "ready";
      fileName.textContent = `${file.name} (pronto)`;
    } catch (error) {
      console.error("Erro ao processar PDF:", error);
      uploadedFileContent = "[Erro ao extrair conteúdo do PDF]";
      fileName.className = "error";
      fileName.textContent = `${file.name} (erro na extração)`;
    }

    isProcessingPDF = false;
  } else {
    uploadedFileContent = "[Tipo de arquivo não suportado]";
    fileName.className = "error";
  }
});

analyzeBtn.addEventListener("click", async () => {
  if (isProcessingPDF) {
    showResponse(
      "⏳ Aguarde, ainda extraindo texto do PDF...",
      "status-processing",
    );
    return;
  }

  showResponse("⏳ Analisando...", "status-processing");
  analyzeBtn.disabled = true;

  try {
    let formData = new FormData();
    let methodLabel = "";
    let contentForHistory = "";

    if (!emailText.disabled && emailText.value.trim()) {
      const blob = new Blob([emailText.value], { type: "text/plain" });
      formData.append("file", blob, "email_digitado.txt");
      methodLabel = "Texto inserido manualmente";
      contentForHistory = emailText.value;
    } else if (fileInput.files.length) {
      const file = fileInput.files[0];
      formData.append("file", file);

      const isPDF = file.name.toLowerCase().endsWith(".pdf");
      const ext = isPDF ? "PDF" : "TXT";
      methodLabel = `Upload via ${ext}`;

      if (
        uploadedFileContent &&
        !uploadedFileContent.includes("[Conteúdo extraído") &&
        !uploadedFileContent.includes("[Tipo de arquivo") &&
        !uploadedFileContent.includes("[Erro ao extrair")
      ) {
        contentForHistory = uploadedFileContent;
      } else if (isPDF) {
        contentForHistory = await extractPDFText(file);
      } else {
        contentForHistory = await readTextFile(file);
      }
    } else {
      showResponse(
        "⚠️ Insira um texto ou selecione um arquivo.",
        "status-error",
      );
      analyzeBtn.disabled = false;
      return;
    }

    const res = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) throw new Error(`Erro no servidor: ${res.status}`);

    const data = await res.json();

    showResponse(
      `
      <div><strong>Categoria:</strong> <span class="category">${data.category}</span></div>
      <div><strong>Resposta:</strong> ${data.response}</div>
      
    `,
      "status-success",
    );

    addHistory(methodLabel, data, contentForHistory);
  } catch (err) {
    console.error("Erro na análise:", err);
    showResponse("❌ Erro ao analisar. Verifique o servidor.", "status-error");
  } finally {
    analyzeBtn.disabled = false;
  }
});

async function extractPDFText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const typedArray = new Uint8Array(e.target.result);

        const loadingTask = pdfjsLib.getDocument(typedArray);
        const pdf = await loadingTask.promise;

        let fullText = "";
        const maxPages = Math.min(pdf.numPages, 10); // Limita a 10 páginas

        for (let i = 1; i <= maxPages; i++) {
          try {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items
              .map((item) => item.str)
              .join(" ");
            fullText += pageText + "\n\n";
          } catch (pageError) {
            console.warn(`Erro na página ${i}:`, pageError);
            fullText += `[Erro ao ler página ${i}]\n\n`;
          }
        }

        if (pdf.numPages > 10) {
          fullText += `\n[Documento truncado: ${pdf.numPages} páginas no total, mostrando apenas as primeiras 10]`;
        }

        resolve(fullText.trim() || "[Não foi possível extrair texto do PDF]");
      } catch (error) {
        console.error("Erro ao processar PDF:", error);
        reject(error);
      }
    };
    reader.onerror = (error) => reject(error);
    reader.readAsArrayBuffer(file);
  });
}

function readTextFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

function showResponse(content, className = "") {
  responseDiv.innerHTML = content;
  responseDiv.className = `response ${className}`;
}

function addHistory(method, data, content) {
  const displayContent = formatContentForDisplay(content);

  history.unshift({
    method,
    category: data.category,
    response: data.response,
    content: displayContent,
    fullContent: content,
    timestamp: new Date().toLocaleTimeString("pt-BR"),
  });

  resetForm();

  renderHistory();
}

function formatContentForDisplay(content) {
  if (!content) return "[Nenhum conteúdo]";

  const maxLength = 1500;
  let displayContent = content;

  if (content.length > maxLength) {
    displayContent =
      content.substring(0, maxLength) + "\n\n...[conteúdo truncado]";
  }

  return displayContent;
}

function resetForm() {
  emailText.value = "";
  emailText.disabled = false;
  fileInput.value = "";
  fileName.textContent = "Nenhum arquivo selecionado";
  fileName.className = "";
  uploadedFileContent = "";
}

function renderHistory() {
  historyDiv.innerHTML = "";

  if (history.length === 0) {
    historyDiv.innerHTML =
      '<div class="no-history">Nenhuma análise realizada ainda.</div>';
    return;
  }

  history.forEach((item, index) => {
    const card = document.createElement("div");
    card.className = "history-card";

    const formattedContent = escapeHtml(item.content).replace(/\n/g, "<br>");
    const formattedResponse = escapeHtml(item.response).replace(/\n/g, "<br>");

    card.innerHTML = `
      <div class="card-header ${openIndex === index ? "open" : ""}">
        <div>
          <strong>${item.method}</strong>
          <span class="timestamp">${item.timestamp}</span>
        </div>
        <div>
          <span class="category-badge">${item.category}</span>
          <span class="toggle-icon">${openIndex === index ? "▼" : "▶"}</span>
        </div>
      </div>
      <div class="card-body ${openIndex === index ? "open" : ""}">
        <div class="content-label">Conteúdo analisado:</div>
        <div class="content-box">${formattedContent}</div>
        
        <div class="response-label">Resposta:</div>
        <div class="response-box">${formattedResponse}</div>
      </div>
    `;

    const header = card.querySelector(".card-header");
    header.addEventListener("click", (e) => {
      if (!e.target.closest(".category-badge")) {
        openIndex = openIndex === index ? null : index;
        renderHistory();
      }
    });

    historyDiv.appendChild(card);
  });
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

renderHistory();

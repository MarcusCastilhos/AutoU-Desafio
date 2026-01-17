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

/* ---------- Upload de Arquivo ---------- */
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

  // Limpa e bloqueia textarea
  emailText.value = "";
  emailText.disabled = true;

  // Verifica o tipo de arquivo
  const isTXT =
    file.type === "text/plain" || file.name.toLowerCase().endsWith(".txt");
  const isPDF =
    file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");

  if (isTXT) {
    // Lê arquivo TXT
    fileName.className = "ready";
    const reader = new FileReader();
    reader.onload = () => {
      uploadedFileContent = reader.result;
    };
    reader.readAsText(file);
  } else if (isPDF) {
    // Processa arquivo PDF
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

/* ---------- Botão Analisar ---------- */
analyzeBtn.addEventListener("click", async () => {
  // Verifica se ainda está processando PDF
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

    /* Verifica a fonte do conteúdo */
    if (!emailText.disabled && emailText.value.trim()) {
      // Texto manual
      const blob = new Blob([emailText.value], { type: "text/plain" });
      formData.append("file", blob, "email_digitado.txt");
      methodLabel = "Texto inserido manualmente";
      contentForHistory = emailText.value;
    } else if (fileInput.files.length) {
      // Upload de arquivo
      const file = fileInput.files[0];
      formData.append("file", file);

      const isPDF = file.name.toLowerCase().endsWith(".pdf");
      const ext = isPDF ? "PDF" : "TXT";
      methodLabel = `Upload via ${ext}`;

      // Obtém conteúdo para histórico
      if (
        uploadedFileContent &&
        !uploadedFileContent.includes("[Conteúdo extraído") &&
        !uploadedFileContent.includes("[Tipo de arquivo") &&
        !uploadedFileContent.includes("[Erro ao extrair")
      ) {
        contentForHistory = uploadedFileContent;
      } else if (isPDF) {
        // Se for PDF e não tiver conteúdo, tenta extrair novamente
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

    // Envia para o backend
    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) throw new Error(`Erro no servidor: ${res.status}`);

    const data = await res.json();

    // Exibe resposta
    showResponse(
      `
      <div><strong>Categoria:</strong> <span class="category">${data.category}</span></div>
      <div><strong>Resposta:</strong> ${data.response}</div>
      
    `,
      "status-success",
    );

    // Adiciona ao histórico
    addHistory(methodLabel, data, contentForHistory);
  } catch (err) {
    console.error("Erro na análise:", err);
    showResponse("❌ Erro ao analisar. Verifique o servidor.", "status-error");
  } finally {
    analyzeBtn.disabled = false;
  }
});

/* ---------- Funções Auxiliares ---------- */

// Extrai texto de PDF usando pdf.js
async function extractPDFText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const typedArray = new Uint8Array(e.target.result);

        // Carrega o PDF
        const loadingTask = pdfjsLib.getDocument(typedArray);
        const pdf = await loadingTask.promise;

        let fullText = "";
        const maxPages = Math.min(pdf.numPages, 10); // Limita a 10 páginas

        // Extrai texto de cada página
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

// Lê arquivo de texto
function readTextFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

// Exibe resposta na interface
function showResponse(content, className = "") {
  responseDiv.innerHTML = content;
  responseDiv.className = `response ${className}`;
}

/* ---------- Gerenciamento do Histórico ---------- */

function addHistory(method, data, content) {
  // Prepara conteúdo para exibição
  const displayContent = formatContentForDisplay(content);

  // Adiciona ao histórico
  history.unshift({
    method,
    category: data.category,
    response: data.response,
    content: displayContent,
    fullContent: content,
    timestamp: new Date().toLocaleTimeString("pt-BR"),
  });

  // Limpa o formulário
  resetForm();

  // Renderiza histórico
  renderHistory();
}

function formatContentForDisplay(content) {
  if (!content) return "[Nenhum conteúdo]";

  // Limita o tamanho para exibição
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

    // Formata o conteúdo para HTML
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

    // Adiciona evento de clique no cabeçalho
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

// Função para escapar HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Inicialização: renderiza histórico vazio
renderHistory();

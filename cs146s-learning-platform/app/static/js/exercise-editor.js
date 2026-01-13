/**
 * Exercise Editor Enhancement
 * Provides autosave, linting, formatting, and improved UX for the exercise editor
 */

class ExerciseAPI {
  constructor(baseUrl = '/api/v1') {
    this.baseUrl = baseUrl;
  }

  async autosave(exerciseId, data) {
    return this.request('POST', `/exercises/${exerciseId}/autosave`, data);
  }

  async lint(exerciseId, code) {
    return this.request('POST', `/exercises/${exerciseId}/lint`, { code });
  }

  async format(exerciseId, code) {
    return this.request('POST', `/exercises/${exerciseId}/format`, { code });
  }

  async execute(exerciseId, data) {
    return this.request('POST', `/exercises/${exerciseId}/execute`, data);
  }

  async submit(exerciseId, data) {
    return this.request('POST', `/exercises/${exerciseId}/submit`, data);
  }

  async request(method, endpoint, data = null) {
    const config = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCsrfToken()
      }
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, config);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content ||
           document.querySelector('[name="csrf_token"]')?.value ||
           '';
  }
}

class AutosaveManager {
  constructor(editor, api, exerciseId) {
    this.editor = editor;
    this.api = api;
    this.exerciseId = exerciseId;
    this.timer = null;
    this.retryCount = 0;
    this.maxRetries = 3;
    this.isOnline = navigator.onLine;
    this.lastSavedContent = '';
  }

  init() {
    // 监听编辑器内容变化
    this.editor.onDidChangeModelContent(() => {
      this.scheduleSave();
    });

    // 监听在线状态变化
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.syncPendingChanges();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });

    // 页面卸载时保存
    window.addEventListener('beforeunload', () => {
      this.saveToLocalStorage();
    });
  }

  scheduleSave() {
    this.debouncedSave();
  }

  debouncedSave = this.debounce(() => {
    this.save();
  }, 1000);

  async save() {
    const content = this.editor.getValue();
    if (content === this.lastSavedContent) {
      return; // 内容未变化
    }

    this.updateUI('saving');

    try {
      // 总是保存到本地存储
      this.saveToLocalStorage();

      // 如果在线，同步到服务器
      if (this.isOnline) {
        const metadata = {
          cursorPosition: this.editor.getPosition(),
          selection: this.editor.getSelection()
        };

        const result = await this.api.autosave(this.exerciseId, {
          code: content,
          metadata: metadata
        });

        if (result.success) {
          this.lastSavedContent = content;
          this.retryCount = 0;
          this.updateUI('saved', result.saved_at);
        } else {
          throw new Error(result.message);
        }
      } else {
        this.updateUI('unsaved');
      }
    } catch (error) {
      console.error('Autosave failed:', error);
      this.retryCount++;

      if (this.retryCount < this.maxRetries) {
        // 指数退避重试
        setTimeout(() => this.save(), Math.pow(2, this.retryCount) * 1000);
      } else {
        this.updateUI('error');
        this.retryCount = 0;
      }
    }
  }

  saveToLocalStorage() {
    const content = this.editor.getValue();
    const key = `exercise_${this.exerciseId}_draft`;
    const data = {
      code: content,
      timestamp: new Date().toISOString(),
      cursorPosition: this.editor.getPosition(),
      selection: this.editor.getSelection()
    };
    localStorage.setItem(key, JSON.stringify(data));
  }

  loadFromLocalStorage() {
    const key = `exercise_${this.exerciseId}_draft`;
    const data = localStorage.getItem(key);
    if (data) {
      try {
        const parsed = JSON.parse(data);
        return parsed;
      } catch (e) {
        console.warn('Invalid localStorage data, clearing...');
        localStorage.removeItem(key);
      }
    }
    return null;
  }

  async syncPendingChanges() {
    if (!this.isOnline) return;

    const localData = this.loadFromLocalStorage();
    if (localData && localData.code !== this.lastSavedContent) {
      try {
        await this.api.autosave(this.exerciseId, {
          code: localData.code,
          metadata: {
            cursorPosition: localData.cursorPosition,
            selection: localData.selection
          }
        });
        this.lastSavedContent = localData.code;
        this.updateUI('saved');
      } catch (error) {
        console.error('Failed to sync pending changes:', error);
      }
    }
  }

  updateUI(status, timestamp = null) {
    const indicator = document.getElementById('autosave-indicator');
    if (!indicator) return;

    indicator.className = `autosave-indicator ${status}`;

    let text = '';
    switch (status) {
      case 'saving':
        text = '保存中...';
        break;
      case 'saved':
        text = timestamp ? `已保存 ${this.formatTimeAgo(timestamp)}` : '已保存';
        break;
      case 'unsaved':
        text = '未保存';
        break;
      case 'error':
        text = '保存失败';
        break;
      default:
        text = '';
    }

    indicator.textContent = text;
  }

  formatTimeAgo(timestamp) {
    const now = new Date();
    const saved = new Date(timestamp);
    const diffMs = now - saved;
    const diffSeconds = Math.floor(diffMs / 1000);

    if (diffSeconds < 60) return `${diffSeconds}秒前`;
    if (diffSeconds < 3600) return `${Math.floor(diffSeconds / 60)}分钟前`;
    return `${Math.floor(diffSeconds / 3600)}小时前`;
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}

class LintManager {
  constructor(editor, api, exerciseId) {
    this.editor = editor;
    this.api = api;
    this.exerciseId = exerciseId;
    this.issues = [];
    this.decorations = [];
    this.isVisible = true;
  }

  init() {
    // 初始检查
    this.scheduleCheck();
  }

  scheduleCheck() {
    this.debouncedCheck();
  }

  debouncedCheck = this.debounce(async () => {
    await this.checkCode();
  }, 500);

  async checkCode() {
    try {
      const code = this.editor.getValue();
      const result = await this.api.lint(this.exerciseId, code);

      if (result.success) {
        this.issues = result.issues || [];
        this.updateDecorations();
        this.updatePanel();
      } else {
        console.warn('Lint check returned error:', result.message);
        this.issues = result.issues || [{
          line: 1,
          column: 1,
          message: result.message || '代码检查失败',
          severity: 'error',
          source: 'system'
        }];
        this.updateDecorations();
        this.updatePanel();
      }
    } catch (error) {
      console.error('Lint check failed:', error);
      this.issues = [{
        line: 1,
        column: 1,
        message: '代码检查服务暂时不可用',
        severity: 'warning',
        source: 'network'
      }];
      this.updateDecorations();
      this.updatePanel();
    }
  }

  updateDecorations() {
    // 清除现有装饰
    this.decorations = this.editor.deltaDecorations(this.decorations, []);

    if (this.issues.length === 0) return;

    const newDecorations = this.issues.map(issue => {
      const lineNumber = Math.max(1, issue.line || 1);
      const column = Math.max(1, issue.column || 1);
      const severity = issue.severity || 'error';

      // 获取该行的内容长度，用于创建适当的装饰范围
      const lineContent = this.editor.getModel().getLineContent(lineNumber);
      const endColumn = Math.min(column + 10, lineContent.length + 1); // 高亮一些字符

      return {
        range: new monaco.Range(lineNumber, column, lineNumber, endColumn),
        options: {
          className: `lint-decoration-${severity}`,
          glyphMarginClassName: `lint-glyph-${severity}`,
          hoverMessage: { value: this.formatHoverMessage(issue) },
          minimap: { color: this.getSeverityColor(severity), position: monaco.editor.MinimapPosition.Gutter }
        }
      };
    });

    this.decorations = this.editor.deltaDecorations([], newDecorations);
  }

  formatHoverMessage(issue) {
    let message = issue.message;
    if (issue.source) {
      message += `\n来源: ${issue.source}`;
    }
    if (issue.severity) {
      message += `\n严重程度: ${this.getSeverityText(issue.severity)}`;
    }
    return message;
  }

  getSeverityColor(severity) {
    switch (severity) {
      case 'error': return { red: 0.8, green: 0.2, blue: 0.2, alpha: 0.6 };
      case 'warning': return { red: 0.8, green: 0.6, blue: 0.2, alpha: 0.6 };
      case 'info': return { red: 0.2, green: 0.6, blue: 0.8, alpha: 0.6 };
      default: return { red: 0.5, green: 0.5, blue: 0.5, alpha: 0.6 };
    }
  }

  getSeverityText(severity) {
    switch (severity) {
      case 'error': return '错误';
      case 'warning': return '警告';
      case 'info': return '信息';
      default: return severity;
    }
  }

  updatePanel() {
    const panel = document.getElementById('lint-panel');
    const header = document.getElementById('lint-header');
    const content = document.getElementById('lint-content');
    const countBadge = document.getElementById('lint-count');

    if (!panel || !header || !content || !countBadge) return;

    // 更新计数和样式
    const errorCount = this.issues.filter(i => i.severity === 'error').length;
    const warningCount = this.issues.filter(i => i.severity === 'warning').length;
    const infoCount = this.issues.filter(i => i.severity === 'info').length;

    countBadge.textContent = this.issues.length;
    countBadge.className = `lint-count ${errorCount > 0 ? 'errors' : warningCount > 0 ? 'warnings' : 'info'}`;

    // 清除现有内容
    content.innerHTML = '';

    if (this.issues.length === 0) {
      content.innerHTML = `
        <div class="text-center text-muted p-4">
          <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
          <div>代码检查通过，没有发现问题。</div>
        </div>
      `;
      return;
    }

    // 按严重程度排序：error > warning > info
    const sortedIssues = this.issues.sort((a, b) => {
      const severityOrder = { 'error': 3, 'warning': 2, 'info': 1 };
      return (severityOrder[b.severity] || 0) - (severityOrder[a.severity] || 0);
    });

    // 添加问题列表
    sortedIssues.forEach((issue, index) => {
      const issueElement = document.createElement('div');
      issueElement.className = `lint-issue ${issue.severity || 'error'}`;

      const originalIndex = this.issues.indexOf(issue);

      issueElement.innerHTML = `
        <div class="lint-issue-icon">
          ${this.getSeverityIcon(issue.severity)}
        </div>
        <div class="lint-issue-content">
          <div class="lint-issue-message">${this.escapeHtml(issue.message)}</div>
          <div class="lint-issue-location">
            第 ${issue.line || 1} 行，第 ${issue.column || 1} 列
            ${issue.source ? ` • ${issue.source}` : ''}
          </div>
        </div>
        <div class="lint-issue-actions">
          <button class="lint-issue-action" onclick="exerciseEditor.lintManager.jumpToIssue(${originalIndex})" title="跳转到代码位置">
            <i class="fas fa-location-arrow"></i>
          </button>
          ${issue.severity === 'error' ? `
            <button class="lint-issue-action" onclick="exerciseEditor.lintManager.showIssueHelp(${originalIndex})" title="获取帮助">
              <i class="fas fa-question-circle"></i>
            </button>
          ` : ''}
        </div>
      `;

      content.appendChild(issueElement);
    });
  }

  showIssueHelp(issueIndex) {
    const issue = this.issues[issueIndex];
    if (!issue) return;

    // 显示一个简单的帮助模态框或提示
    const helpText = this.getIssueHelpText(issue);
    alert(`问题帮助:\n\n${helpText}`);
  }

  getIssueHelpText(issue) {
    // 基于问题类型提供帮助信息
    if (issue.message.includes('语法错误')) {
      return '检查代码语法：确保括号匹配、缩进正确、语句完整。';
    } else if (issue.message.includes('未定义')) {
      return '变量未定义：确保在使用变量前先定义它，或者检查拼写是否正确。';
    } else if (issue.message.includes('缩进')) {
      return '缩进错误：Python 使用缩进表示代码块，确保一致使用空格或制表符。';
    } else {
      return '请检查代码逻辑和语法，尝试运行代码查看具体错误信息。';
    }
  }

  getSeverityIcon(severity) {
    switch (severity) {
      case 'error': return '⚠️';
      case 'warning': return '⚡';
      case 'info': return 'ℹ️';
      default: return '⚠️';
    }
  }

  jumpToIssue(issueIndex) {
    const issue = this.issues[issueIndex];
    if (issue) {
      this.editor.revealLine(issue.line || 1);
      this.editor.setPosition({ lineNumber: issue.line || 1, column: issue.column || 1 });
      this.editor.focus();
    }
  }

  togglePanel() {
    const panel = document.getElementById('lint-panel');
    const content = document.getElementById('lint-content');

    if (!panel || !content) return;

    this.isVisible = !this.isVisible;

    if (this.isVisible) {
      content.style.display = 'block';
      panel.classList.remove('collapsed');
    } else {
      content.style.display = 'none';
      panel.classList.add('collapsed');
    }
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}

class ExerciseEditor {
  constructor(options) {
    this.exerciseId = options.exerciseId;
    this.api = new ExerciseAPI();
    this.autosaveManager = null;
    this.lintManager = null;
    this.editor = null;
    this.currentAttemptNumber = 1;
  }

  async init() {
    await this.initMonaco();
    this.setupManagers();
    this.setupEventListeners();
    this.loadDraft();
    this.setupKeyboardShortcuts();
    this.initSettingsIndicators();
  }

  async initMonaco() {
    return new Promise((resolve) => {
      require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' } });

      require(['vs/editor/editor.main'], () => {
        this.editor = monaco.editor.create(document.getElementById('editor-container'), {
          value: this.getInitialCode(),
          language: 'python',
          theme: this.getPreferredTheme(),
          fontSize: 14,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: this.getPreferredTabSize(),
          insertSpaces: this.getPreferredInsertSpaces(),
          wordWrap: 'on',
          lineNumbers: this.getPreferredLineNumbers() ? 'on' : 'off',
          glyphMargin: true, // 为lint装饰留出空间
          lightbulb: { enabled: true }
        });

        resolve();
      });
    });
  }

  setupManagers() {
    this.autosaveManager = new AutosaveManager(this.editor, this.api, this.exerciseId);
    this.lintManager = new LintManager(this.editor, this.api, this.exerciseId);

    this.autosaveManager.init();
    this.lintManager.init();
  }

  setupEventListeners() {
    // 运行按钮
    const runBtn = document.getElementById('runCodeBtn');
    if (runBtn) {
      runBtn.addEventListener('click', () => this.runCode());
    }

    // 提交按钮
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => this.submitCode());
    }

    // 格式化按钮
    const formatBtn = document.getElementById('formatCodeBtn');
    if (formatBtn) {
      formatBtn.addEventListener('click', () => this.formatCode());
    }

    // 设置按钮
    const settingsBtn = document.getElementById('editorSettingsBtn');
    if (settingsBtn) {
      settingsBtn.addEventListener('click', () => this.toggleSettings());
    }

    // Lint面板切换
    const lintToggle = document.getElementById('lint-toggle');
    if (lintToggle) {
      lintToggle.addEventListener('click', () => this.lintManager.togglePanel());
    }
  }

  setupKeyboardShortcuts() {
    // 代码执行和保存
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => this.runCode());
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => this.saveCode());

    // 代码格式化
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyF, () => this.formatCode());

    // 注释切换
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.US_SLASH, () => this.toggleComment());

    // 主题切换
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyT, () => this.toggleTheme());

    // 行号切换
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyL, () => this.toggleLineNumbers());

    // 重新检查代码
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyC, () => {
      if (this.lintManager) {
        this.lintManager.scheduleCheck();
      }
    });

    // 显示快捷键帮助
    this.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyH, () => this.showKeyboardShortcuts());
  }

  toggleTheme() {
    const currentTheme = this.editor.getOption(monaco.editor.EditorOption.theme);
    const newTheme = currentTheme === 'vs-light' ? 'vs-dark' : 'vs-light';

    this.editor.updateOptions({ theme: newTheme });
    localStorage.setItem('editor-theme', newTheme);

    // 更新UI指示器
    this.updateThemeIndicator(newTheme);
  }

  toggleLineNumbers() {
    const currentLineNumbers = this.editor.getOption(monaco.editor.EditorOption.lineNumbers).renderType;
    const newLineNumbers = currentLineNumbers === monaco.editor.RenderLineNumbersType.On ? monaco.editor.RenderLineNumbersType.Off : monaco.editor.RenderLineNumbersType.On;

    this.editor.updateOptions({ lineNumbers: newLineNumbers });
    localStorage.setItem('editor-line-numbers', newLineNumbers === monaco.editor.RenderLineNumbersType.On);

    // 更新UI指示器
    this.updateLineNumbersIndicator(newLineNumbers === monaco.editor.RenderLineNumbersType.On);
  }

  updateThemeIndicator(theme) {
    // 可以添加一个小的主题指示器到工具栏
    const themeIndicator = document.getElementById('theme-indicator');
    if (themeIndicator) {
      themeIndicator.innerHTML = theme === 'vs-dark' ? '🌙' : '☀️';
      themeIndicator.title = `当前主题: ${theme === 'vs-dark' ? '深色' : '浅色'}`;
    }
  }

  updateLineNumbersIndicator(showLineNumbers) {
    // 可以添加行号指示器
    const lineNumbersIndicator = document.getElementById('line-numbers-indicator');
    if (lineNumbersIndicator) {
      lineNumbersIndicator.innerHTML = showLineNumbers ? '🔢' : '📄';
      lineNumbersIndicator.title = `行号: ${showLineNumbers ? '显示' : '隐藏'}`;
    }
  }

  showKeyboardShortcuts() {
    const shortcuts = [
      { key: 'Ctrl+Enter', action: '运行代码' },
      { key: 'Ctrl+S', action: '保存代码' },
      { key: 'Ctrl+Shift+F', action: '格式化代码' },
      { key: 'Ctrl+/', action: '切换注释' },
      { key: 'Ctrl+Shift+T', action: '切换主题' },
      { key: 'Ctrl+Shift+L', action: '切换行号' },
      { key: 'Ctrl+Shift+C', action: '重新检查代码' },
      { key: 'Ctrl+Shift+H', action: '显示快捷键帮助' }
    ];

    let shortcutsHtml = '<div class="keyboard-shortcuts">';
    shortcutsHtml += '<h5>键盘快捷键</h5>';
    shortcutsHtml += '<table class="table table-sm">';
    shortcutsHtml += '<thead><tr><th>快捷键</th><th>功能</th></tr></thead>';
    shortcutsHtml += '<tbody>';

    shortcuts.forEach(shortcut => {
      shortcutsHtml += `<tr><td><kbd>${shortcut.key}</kbd></td><td>${shortcut.action}</td></tr>`;
    });

    shortcutsHtml += '</tbody></table></div>';

    // 使用简单的alert显示，也可以创建一个模态框
    const helpWindow = window.open('', 'keyboard-shortcuts', 'width=400,height=500,scrollbars=yes,resizable=yes');
    if (helpWindow) {
      helpWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>键盘快捷键</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
          <style>
            body { padding: 20px; }
            .keyboard-shortcuts { max-width: none; }
            kbd { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 3px; padding: 2px 4px; font-size: 0.875em; }
          </style>
        </head>
        <body>
          ${shortcutsHtml}
        </body>
        </html>
      `);
      helpWindow.document.close();
    } else {
      // 如果弹窗被阻止，使用alert
      alert('键盘快捷键帮助:\n\n' +
        shortcuts.map(s => `${s.key}: ${s.action}`).join('\n')
      );
    }
  }

  async runCode() {
    const runBtn = document.getElementById('runCodeBtn');
    const code = this.editor.getValue();

    this.setButtonState(runBtn, 'running', '运行中...');

    try {
      // 先进行lint检查
      if (this.lintManager.issues.some(issue => issue.severity === 'error')) {
        if (!confirm('代码存在错误，确定要运行吗？')) {
          this.setButtonState(runBtn, 'idle', '运行代码');
          return;
        }
      }

      const result = await this.api.execute(this.exerciseId, { code });
      this.displayExecutionResult(result.result);

    } catch (error) {
      console.error('Execution failed:', error);
      this.displayExecutionResult({
        success: false,
        error: '执行失败，请稍后重试'
      });
    }

    this.setButtonState(runBtn, 'idle', '运行代码');
  }

  async submitCode() {
    if (!confirm('确定要提交答案吗？提交后将无法修改。')) {
      return;
    }

    const submitBtn = document.getElementById('submitBtn');
    const code = this.editor.getValue();

    this.setButtonState(submitBtn, 'running', '提交中...');

    try {
      const result = await this.api.submit(this.exerciseId, {
        code: code,
        attempt_number: this.currentAttemptNumber
      });

      if (result.success) {
        alert(`提交成功！得分: ${result.score}\n${result.is_correct ? '✓ 答案正确' : '✗ 答案错误'}`);
        this.currentAttemptNumber++;
        this.loadSubmissionHistory();
        this.loadProgress();
      } else {
        alert('提交失败: ' + (result.message || '未知错误'));
      }

    } catch (error) {
      console.error('Submission failed:', error);
      alert('网络错误，请稍后重试');
    }

    this.setButtonState(submitBtn, 'idle', '提交答案');
  }

  async formatCode() {
    const formatBtn = document.getElementById('formatCodeBtn');
    const code = this.editor.getValue();

    this.setButtonState(formatBtn, 'running', '格式化中...');

    try {
      const result = await this.api.format(this.exerciseId, { code });

      if (result.success) {
        this.editor.setValue(result.code);
        this.autosaveManager.scheduleSave();
        // 重新检查代码
        if (this.lintManager) {
          setTimeout(() => this.lintManager.scheduleCheck(), 500);
        }
      } else {
        // 如果格式化未启用或失败，使用客户端回退
        if (result.message && result.message.includes('未启用')) {
          this.fallbackFormat();
        } else {
          alert('格式化失败: ' + (result.message || '未知错误'));
        }
      }

    } catch (error) {
      console.error('Formatting failed:', error);
      // 回退到客户端简单格式化
      this.fallbackFormat();
    }

    this.setButtonState(formatBtn, 'idle', '格式化');
  }

  fallbackFormat() {
    // 简单的客户端格式化作为回退
    const code = this.editor.getValue();
    // 这里可以实现基本的Python格式化逻辑
    // 目前只是重新缩进
    const lines = code.split('\n');
    const formattedLines = lines.map(line => line.trimEnd());
    this.editor.setValue(formattedLines.join('\n'));
  }

  saveCode() {
    this.autosaveManager.scheduleSave();
  }

  toggleComment() {
    const selection = this.editor.getSelection();
    const model = this.editor.getModel();
    const lines = [];

    for (let i = selection.startLineNumber; i <= selection.endLineNumber; i++) {
      lines.push(i);
    }

    // 检查是否所有行都以#开头
    const allCommented = lines.every(lineNumber => {
      const lineContent = model.getLineContent(lineNumber);
      return lineContent.trim().startsWith('#') || lineContent.trim() === '';
    });

    // 切换注释
    this.editor.getModel().pushEditOperations(
      [],
      lines.map(lineNumber => {
        const lineContent = model.getLineContent(lineNumber);
        const trimmed = lineContent.trim();

        if (allCommented && trimmed.startsWith('#')) {
          // 取消注释
          const commentIndex = lineContent.indexOf('#');
          return {
            range: new monaco.Range(lineNumber, 1, lineNumber, commentIndex + 1),
            text: ''
          };
        } else if (!allCommented && trimmed) {
          // 添加注释
          return {
            range: new monaco.Range(lineNumber, 1, lineNumber, 1),
            text: '# '
          };
        }
        return null;
      }).filter(op => op !== null),
      () => null
    );
  }

  toggleSettings() {
    const menu = document.getElementById('settings-menu');
    if (menu) {
      menu.classList.toggle('show');
    }
  }

  setButtonState(button, state, text) {
    if (!button) return;

    button.disabled = state === 'running';
    button.innerHTML = text;

    // 更新类名用于样式
    button.className = button.className.replace(/\s+(success|danger|primary)/g, '');
    if (state === 'running') {
      button.classList.add('primary');
    } else {
      button.classList.add('success');
    }
  }

  displayExecutionResult(result) {
    const outputPanel = document.getElementById('output-panel');
    if (!outputPanel) return;

    let html = '';

    if (result.success) {
      html += '<div class="alert alert-success"><i class="fas fa-check-circle"></i> 执行成功</div>';

      if (result.stdout) {
        html += `
          <div class="output-content">
            <pre class="stdout">${this.escapeHtml(result.stdout)}</pre>
          </div>
        `;
      }
    } else {
      html += `
        <div class="alert alert-danger">
          <i class="fas fa-times-circle"></i> 执行失败
          <br><strong>错误信息:</strong> ${this.escapeHtml(result.error || '未知错误')}
        </div>
      `;
    }

    if (result.stderr) {
      html += `
        <div class="output-content">
          <pre class="stderr">${this.escapeHtml(result.stderr)}</pre>
        </div>
      `;
    }

    // 添加执行信息
    if (result.execution_time) {
      html += `
        <div class="execution-info">
          <span class="time"><i class="fas fa-clock"></i> 执行时间: ${result.execution_time.toFixed(2)}秒</span>
          <span class="status success">完成</span>
        </div>
      `;
    }

    outputPanel.innerHTML = html;
  }

  loadDraft() {
    const draft = this.autosaveManager.loadFromLocalStorage();
    if (draft && draft.code) {
      if (confirm('发现未保存的草稿，是否加载？')) {
        this.editor.setValue(draft.code);
        if (draft.cursorPosition) {
          this.editor.setPosition(draft.cursorPosition);
        }
        if (draft.selection) {
          this.editor.setSelection(draft.selection);
        }
      }
    }
  }

  loadProgress() {
    // 重新加载进度信息
    fetch(`/api/v1/learning/progress/{{ exercise.week_id }}`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // 更新进度显示
          console.log('Progress updated:', data.progress);
        }
      })
      .catch(error => console.error('Failed to load progress:', error));
  }

  loadSubmissionHistory() {
    // 重新加载提交历史
    fetch(`/api/v1/exercises/{{ exercise.id }}/submissions`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // 更新历史显示
          console.log('Submission history updated:', data.submissions);
        }
      })
      .catch(error => console.error('Failed to load submission history:', error));
  }

  getInitialCode() {
    // 从模板变量获取初始代码
    return document.getElementById('initial-code')?.textContent ||
           document.querySelector('[data-initial-code]')?.dataset.initialCode ||
           '# 请在这里编写代码\nprint("Hello World!")';
  }

  getPreferredTheme() {
    return localStorage.getItem('editor-theme') || 'vs-light';
  }

  getPreferredTabSize() {
    return parseInt(localStorage.getItem('editor-tab-size')) || 4;
  }

  getPreferredInsertSpaces() {
    return localStorage.getItem('editor-insert-spaces') !== 'false';
  }

  getPreferredLineNumbers() {
    return localStorage.getItem('editor-line-numbers') !== 'false';
  }

  setTabSize(size) {
    this.editor.updateOptions({
      tabSize: size,
      insertSpaces: this.getPreferredInsertSpaces()
    });
    localStorage.setItem('editor-tab-size', size);
  }

  initSettingsIndicators() {
    // 初始化设置指示器
    const theme = this.getPreferredTheme();
    this.updateThemeIndicator(theme);

    const showLineNumbers = this.getPreferredLineNumbers();
    this.updateLineNumbersIndicator(showLineNumbers);

    // 更新菜单文本
    this.updateSettingsMenuText();
  }

  updateSettingsMenuText() {
    const themeText = document.getElementById('theme-text');
    const lineNumbersText = document.getElementById('line-numbers-text');

    if (themeText) {
      const currentTheme = this.editor.getOption(monaco.editor.EditorOption.theme);
      themeText.textContent = currentTheme === 'vs-light' ? '切换到深色主题' : '切换到浅色主题';
    }

    if (lineNumbersText) {
      const currentLineNumbers = this.editor.getOption(monaco.editor.EditorOption.lineNumbers).renderType;
      lineNumbersText.textContent = currentLineNumbers === monaco.editor.RenderLineNumbersType.On ? '隐藏行号' : '显示行号';
    }
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // 公共方法供外部调用
  jumpToIssue(issueIndex) {
    this.lintManager.jumpToIssue(issueIndex);
  }
}

// 全局实例
let exerciseEditor = null;

// 初始化函数
function initExerciseEditor(exerciseId) {
  exerciseEditor = new ExerciseEditor({ exerciseId });
  exerciseEditor.init().catch(error => {
    console.error('Failed to initialize exercise editor:', error);
  });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  const exerciseId = parseInt(document.querySelector('[data-exercise-id]')?.dataset.exerciseId ||
                              window.location.pathname.split('/').pop());
  if (exerciseId) {
    initExerciseEditor(exerciseId);
  }
});

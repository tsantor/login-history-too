'use strict';

const logins = {
  /**
   * aceEditor
   *
   * Turn specific textareas into an ACE editor
   */
  aceEditor: function () {
    ace.config.set('basePath', '/static/js/ace-builds');

    function prettifyJSON(string, indent = 2) {
      try {
        const obj = JSON.parse(string);
        return JSON.stringify(obj, null, indent);
      } catch (e) {
        console.error('Error parsing JSON:', e);
        return string;
      }
    }

    const textareas = document.querySelectorAll('textarea[data-editor]');
    textareas.forEach((textarea) => {
      // Create a div for ace editor
      const mode = textarea.dataset.editor;
      const editDiv = document.createElement('div');

      // Set styles directly
      editDiv.style.position = 'absolute';
      editDiv.style.width = '100%';
      editDiv.style.height = `${textarea.offsetHeight + 15}px`;

      // Insert before textarea
      textarea.parentNode.insertBefore(editDiv, textarea);
      textarea.style.display = 'none';

      // Try to prettify the JSON
      const pretty = prettifyJSON(textarea.value);

      // Create ace editor
      const editor = ace.edit(editDiv);
      editor.setAutoScrollEditorIntoView(true);
      editor.renderer.setShowGutter(textarea.dataset.gutter === 'true');
      editor.renderer.setShowPrintMargin(false);
      editor.getSession().setValue(pretty);
      editor.getSession().setMode(`ace/mode/${mode}`);
      editor.getSession().setTabSize(2);
      editor.getSession().setUseWrapMode(true);
      editor.setTheme('ace/theme/chrome');

      // Copy back to textarea on form submit
      const form = textarea.closest('form');
      if (form) {
        form.addEventListener('submit', () => {
          textarea.value = editor.getSession().getValue();
        });
      }
    });
  },

  initHighlights: function () {
    const uaDataField = document.querySelector('div.field-ua_data');
    const ipDataField = document.querySelector('div.field-ip_data');
    const elementsToHighlight = [];

    if (uaDataField) {
      const uaReadonly = uaDataField.querySelector('div.readonly');
      if (uaReadonly) {
        uaReadonly.style.padding = '6px';
        elementsToHighlight.push(uaReadonly);
      }
    }

    if (ipDataField) {
      const ipReadonly = ipDataField.querySelector('div.readonly');
      if (ipReadonly) {
        ipReadonly.style.padding = '6px';
        elementsToHighlight.push(ipReadonly);
      }
    }

    elementsToHighlight.forEach((el) => {
      hljs.highlightElement(el);
    });
  },

  initAce: function () {
    // const uaDataElement = document.getElementById('id_ua_data');
    // if (uaDataElement) {
    //   uaDataElement.setAttribute('data-editor', 'json');
    //   uaDataElement.setAttribute('data-gutter', 'true');
    // }
    // const ipDataElement = document.getElementById('id_ip_data');
    // if (ipDataElement) {
    //   ipDataElement.setAttribute('data-editor', 'json');
    //   ipDataElement.setAttribute('data-gutter', 'true');
    // }
    // scans.aceEditor();
  },
};

// Use DOMContentLoaded instead of window.onload for better performance
document.addEventListener('DOMContentLoaded', () => {
  // logins.initAce();
  logins.initHighlights();
});

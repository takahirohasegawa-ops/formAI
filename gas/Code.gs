/**
 * Form AI - Google Apps Script
 *
 * スプレッドシートからフォーム自動送信を実行するスクリプト
 * Backend: Python + Browser Use + Google Gemini API
 *
 * 【スプレッドシート構成】
 * A列: URL
 * B列: メッセージ
 * C列: ステータス (空白/送信中/成功/失敗/CAPTCHA/エラー)
 * D列: 詳細
 * E列: コスト
 */

// === 設定 ===
const API_ENDPOINT = 'https://your-railway-app.railway.app/api/submit';
// Railwayデプロイ後、上記のURLを実際のURLに変更してください

// === メニューに追加 ===
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('📧 Form AI')
      .addItem('🚀 選択行を送信', 'submitSelectedRows')
      .addItem('📊 全件送信', 'submitAllRows')
      .addItem('🔄 ステータスクリア', 'clearStatus')
      .addItem('⚙️ 設定', 'showSettings')
      .addToUi();
}

/**
 * 選択された行のフォームを送信
 */
function submitSelectedRows() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const selection = sheet.getActiveRange();
  const startRow = selection.getRow();
  const numRows = selection.getNumRows();

  // ヘッダー行は除外
  if (startRow === 1) {
    SpreadsheetApp.getUi().alert('ヘッダー行は選択しないでください');
    return;
  }

  const ui = SpreadsheetApp.getUi();
  const response = ui.alert(
    `${numRows}行を送信します`,
    `選択された${numRows}件のフォームを送信しますか?`,
    ui.ButtonSet.YES_NO
  );

  if (response !== ui.Button.YES) {
    return;
  }

  submitRows(sheet, startRow, numRows);
}

/**
 * 全件送信（ステータスが空白の行のみ）
 */
function submitAllRows() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const lastRow = sheet.getLastRow();

  if (lastRow <= 1) {
    SpreadsheetApp.getUi().alert('送信するデータがありません');
    return;
  }

  const ui = SpreadsheetApp.getUi();
  const response = ui.alert(
    '全件送信',
    'ステータスが空白の全行を送信しますか?',
    ui.ButtonSet.YES_NO
  );

  if (response !== ui.Button.YES) {
    return;
  }

  // ステータスが空白の行のみ送信
  const statusRange = sheet.getRange(2, 3, lastRow - 1, 1);
  const statusValues = statusRange.getValues();

  let count = 0;
  for (let i = 0; i < statusValues.length; i++) {
    if (statusValues[i][0] === '') {
      const row = i + 2; // ヘッダー分+1、インデックス分+1
      submitRows(sheet, row, 1);
      count++;

      // APIレート制限対策: 1件ごとに少し待つ
      Utilities.sleep(2000);
    }
  }

  SpreadsheetApp.getUi().alert(`${count}件の送信が完了しました`);
}

/**
 * 指定された行のフォームを送信
 */
function submitRows(sheet, startRow, numRows) {
  for (let i = 0; i < numRows; i++) {
    const row = startRow + i;

    // データ取得
    const url = sheet.getRange(row, 1).getValue();
    const message = sheet.getRange(row, 2).getValue();

    // バリデーション
    if (!url || !message) {
      sheet.getRange(row, 3).setValue('エラー');
      sheet.getRange(row, 4).setValue('URLまたはメッセージが空です');
      continue;
    }

    // ステータスを「送信中」に更新
    sheet.getRange(row, 3).setValue('送信中...');
    SpreadsheetApp.flush();

    try {
      // APIリクエスト
      const result = callFormAPI(url, message);

      // 結果を書き込み
      if (result.status === 'success') {
        sheet.getRange(row, 3).setValue('✅ 成功');
        sheet.getRange(row, 3).setBackground('#d4edda');
      } else if (result.status === 'captcha_detected') {
        sheet.getRange(row, 3).setValue('🔒 CAPTCHA');
        sheet.getRange(row, 3).setBackground('#fff3cd');
      } else if (result.status === 'failed') {
        sheet.getRange(row, 3).setValue('❌ 失敗');
        sheet.getRange(row, 3).setBackground('#f8d7da');
      } else {
        sheet.getRange(row, 3).setValue('⚠️ エラー');
        sheet.getRange(row, 3).setBackground('#f8d7da');
      }

      sheet.getRange(row, 4).setValue(result.details || result.message);

      // コスト情報
      if (result.cost_estimate) {
        sheet.getRange(row, 5).setValue(`$${result.cost_estimate.toFixed(6)}`);
      }

    } catch (error) {
      sheet.getRange(row, 3).setValue('⚠️ エラー');
      sheet.getRange(row, 3).setBackground('#f8d7da');
      sheet.getRange(row, 4).setValue(error.toString());
    }

    SpreadsheetApp.flush();

    // レート制限対策
    if (i < numRows - 1) {
      Utilities.sleep(2000);
    }
  }
}

/**
 * Form AI APIを呼び出し
 */
function callFormAPI(url, message) {
  const payload = {
    url: url,
    message: message,
    use_complex_model: false  // 複雑なフォームの場合はtrueに変更
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(API_ENDPOINT, options);
  const responseCode = response.getResponseCode();

  if (responseCode !== 200) {
    throw new Error(`API Error: ${responseCode} - ${response.getContentText()}`);
  }

  return JSON.parse(response.getContentText());
}

/**
 * ステータス列をクリア
 */
function clearStatus() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const lastRow = sheet.getLastRow();

  if (lastRow <= 1) {
    return;
  }

  const ui = SpreadsheetApp.getUi();
  const response = ui.alert(
    'ステータスクリア',
    'すべてのステータスをクリアしますか?',
    ui.ButtonSet.YES_NO
  );

  if (response !== ui.Button.YES) {
    return;
  }

  // C列〜E列をクリア
  const range = sheet.getRange(2, 3, lastRow - 1, 3);
  range.clearContent();
  range.setBackground(null);

  SpreadsheetApp.getUi().alert('ステータスをクリアしました');
}

/**
 * 設定ダイアログを表示
 */
function showSettings() {
  const ui = SpreadsheetApp.getUi();
  const currentEndpoint = API_ENDPOINT;

  const html = `
    <div style="padding: 20px; font-family: Arial, sans-serif;">
      <h2>⚙️ Form AI 設定</h2>
      <p><strong>現在のAPIエンドポイント:</strong></p>
      <p style="background: #f0f0f0; padding: 10px; border-radius: 5px; word-break: break-all;">
        ${currentEndpoint}
      </p>
      <hr>
      <h3>設定変更方法</h3>
      <ol>
        <li>拡張機能 → Apps Script を開く</li>
        <li>Code.gs ファイルを開く</li>
        <li>上部の API_ENDPOINT を編集</li>
        <li>保存</li>
      </ol>
    </div>
  `;

  const htmlOutput = HtmlService.createHtmlOutput(html)
      .setWidth(500)
      .setHeight(300);

  ui.showModalDialog(htmlOutput, 'Form AI 設定');
}

/**
 * スプレッドシートのセットアップ
 */
function setupSheet() {
  const sheet = SpreadsheetApp.getActiveSheet();

  // ヘッダー設定
  const headers = ['URL', 'メッセージ', 'ステータス', '詳細', 'コスト'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // ヘッダーのスタイル設定
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4285f4');
  headerRange.setFontColor('#ffffff');
  headerRange.setFontWeight('bold');
  headerRange.setHorizontalAlignment('center');

  // 列幅設定
  sheet.setColumnWidth(1, 400); // URL
  sheet.setColumnWidth(2, 400); // メッセージ
  sheet.setColumnWidth(3, 120); // ステータス
  sheet.setColumnWidth(4, 300); // 詳細
  sheet.setColumnWidth(5, 100); // コスト

  // サンプルデータ
  const sampleData = [
    ['https://example.com/contact', '貴社のサービスに興味があります。詳細を教えてください。', '', '', ''],
    ['https://example2.com/inquiry', 'お問い合わせです。', '', '', '']
  ];

  sheet.getRange(2, 1, sampleData.length, 5).setValues(sampleData);

  SpreadsheetApp.getUi().alert('✅ セットアップ完了!\n\nメニューから「Form AI」を選択して送信できます。');
}

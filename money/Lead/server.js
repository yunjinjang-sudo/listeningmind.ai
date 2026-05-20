const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;

http.createServer((req, res) => {
  const filePath = path.join(__dirname, '회원목록_변환기.html');
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end('파일 없음'); return; }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(data);
  });
}).listen(PORT, '127.0.0.1', () => {
  console.log(`✅ 서버 실행 중: http://localhost:${PORT}`);
  console.log('종료하려면 Ctrl+C 를 누르세요.');
});

import http from 'k6/http';

export const options = {
  vus: 100,      // 100 người dùng ảo
  duration: '2m' // chạy trong 2 phút
};

export default function () {
  http.get('http://fastapi.local/health');
}
import axios from "axios";
import { baseUrl } from "./constants";

const instance = axios.create({
  // 서버 주소가 기본 적용됨
  baseURL: baseUrl,
});

export default instance;

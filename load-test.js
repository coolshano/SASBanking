import http from "k6/http";
import { sleep } from "k6";

export let options = {
  vus: 3000,          // 1000 virtual users
  duration: "3000s",    // run for 30 seconds
};

export default function () {
  http.get("https://www.aethenos.com");
  sleep(1);
}


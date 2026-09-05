// 로깅을 일괄적으로 해주기 (영어만 이용해야할듯)

import { currTime } from "./date.js";

export default function logger(eventSource, message) {
  console.log(`[${currTime()}] [${eventSource}] ${message}`)
}
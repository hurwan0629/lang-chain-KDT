// cors 설정 여기에서 직접 설정하기

import config from "./env.js"

export const corsOptions = {
  origin: `${config.client.protocol}://${config.client.address}:${config.client.port}`,
  credentials: true
}
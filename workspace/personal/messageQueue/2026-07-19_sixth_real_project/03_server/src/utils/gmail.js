import nodemailer from "nodemailer"
import config from "../config/env.js";
import logger from "./logger.js";

const transporter = nodemailer.createTransport({
    service: "gmail",

    auth: {
        user: config.gmail.user,
        pass: config.gmail.appPassword
    }
})

export async function connectEmail() {
    await transporter.verify()
    logger("/utils/gmail.js connectEmail", "Gmail SMTP Conneceted")
}

export async function sendEmail({to, subject, text=undefined, html=undefined}) {
    const result = await transporter.sendMail({
        from: `"HURWAN" <${config.gmail.user}>`,
        to,
        subject,
        text,
        html
    })
    logger("/utils/gmail.js connectEmail", `result.messageId: ${result.messageId}`)
    logger("/utils/gmail.js connectEmail", `result.accepted: ${result.accepted}`)
    logger("/utils/gmail.js connectEmail", `result.rejected: ${result.rejected}`)

    return result
}
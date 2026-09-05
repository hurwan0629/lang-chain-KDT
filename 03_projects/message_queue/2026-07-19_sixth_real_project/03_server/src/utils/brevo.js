import {BrevoClient} from "@getbrevo/brevo";
import config from "../config/env.js";
import logger from "./logger.js";

const brevo = new BrevoClient({ apiKey: config.brevo.apiKey })


/**
 *
 * @param param0
 * @param param0.subject title
 * @param param0.htmlContent html string
 * @param param0.sender { name: string, email: string}
 * @param param0.to [{ name: string, email: string}, ...]
 * @returns {Promise<void>}
 */
export default async function sendEmail({ subject, htmlContent, to}) {

    const sender = { name: "hurwan", email: "hurwan0629@gmail.com" }

    logger("/utils/brevo.js sendEmail",
`subject: ${subject}
sender: ${JSON.stringify(sender)}
to: ${JSON.stringify(to)}`)
    return await brevo.transactionalEmails.sendTransacEmail({
        subject,
        htmlContent,
        sender,
        to
    })
}
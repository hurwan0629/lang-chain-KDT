import pool from "../config/db.js";
import logger from "../utils/logger.js";

export async function getUserById(id) {
  try {
    const result = await pool.query(`
      SELECT 
        pk, id, name, 
        password_hash as "passwordHash",  
        role, email, address, 
        created_at as "createdAt", 
        updated_at as "updatedAt"
      FROM 
        users
      WHERE
        id = $1
        AND deleted_at IS NOT NULL
      `, [id])
    
    return result.rows[0] ?? null
  } catch (error) {
    logger("/repository/users.repository.js getUserById",
      `error: ${error}`
    )
    throw error
  }
}

export async function checkUserIdExists(id) {
  try {
    const result = await pool.query(`
      SELECT EXISTS ( SELECT 1 FROM users WHERE id = $1 ) AS exists
    `, [id])

    return result.rows[0].exists
  } catch (error) {
    logger("/repository/users.repository.js checkUserIdExists",
        `error: ${error}`
    )
    throw error
  }
}

export async function createUser({id, passwordHash, name, email, address}) {
  try {
    const result = await pool.query(`
      INSERT INTO users(id, password_hash, name, email, address) 
      VALUES ($1, $2, $3, $4, $5)
      RETURNING id, name, email, created_at as createdAt, role
    `, [id, passwordHash, name, email, address])

    return result.rows[0] ?? null
  } catch (error) {
    logger("/repository/users.repository.js createUser",
        `error: ${error}`
    )
    throw error
  }
}
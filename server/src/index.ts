import { Elysia } from "elysia";
import { cors } from "@elysiajs/cors";
import { csv2json, json2csv } from "json-2-csv";

const db = Bun.file("db.csv");

const app = new Elysia()
  .use(cors())
  .get("/suites", async () => {
    const suites = await db.text();
    return csv2json(suites);
  })
  .post(
    "/suites",
    async ({ body }) => {
      const result = json2csv(body);
      await Bun.write(db, result);
      return "Success";
    },
    {
      error: ({ error }) => console.error(error),
    },
  );
app.listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`,
);

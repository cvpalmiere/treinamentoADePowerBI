import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "exercicios/01-carmem-sandiego/gabarito/schema.prisma",
  datasource: {
    url: env("DATABASE_URL"),
  },
});
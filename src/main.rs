mod cli;
mod commands;
mod config;
mod mask;
mod proxy;

use anyhow::Result;
use clap::Parser;
use cli::{Cli, Commands};

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Run(args) => commands::run::execute(args).await,
        Commands::Init => commands::init::execute(),
        Commands::Set(args) => commands::set::execute(args),
        Commands::Status => commands::status::execute(),
    }
}
